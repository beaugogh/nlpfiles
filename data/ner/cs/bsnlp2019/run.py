# original entity types mapped:
# ○ persons (PER) -> PER
# ○ organizations (ORG) -> ORG
# ○ locations (LOC) -> LOC
# ○ events (EVT) -> MISC
# ○ products (PRO) -> MISC

ent_type_map = {
    'PER': 'PER',
    'ORG': 'ORG',
    'LOC': 'LOC',
    'EVT': 'MISC',
    'PRO': 'MISC'
}


def parse_annt_file(annt_file_path):
    # return tuples of (entity_text, entity_type)
    f = open(annt_file_path, 'r', encoding='utf8')
    result = []
    for l in f:
        l = l.replace('\n', '').strip()
        parts = l.split('\t')
        if len(parts) == 4:
            text = parts[0]
            ent_type = ent_type_map[parts[2]]
            result.append((text, ent_type))
    f.close()
    return result


# apath = 'original/test/annotated/nord-stream_CZ-new.xml_file_30000.out'
# parse_annt_file(apath)

def parse_raw_file(raw_file_path, stanza_nlp):
    # return a list of sentences
    started = False
    result = []
    f = open(raw_file_path, 'r', encoding='utf8')
    for l in f:
        if started:
            l = l.replace('\n', '').strip()
            if len(l) > 1:
                doc = stanza_nlp(l)
                for sent in doc.sentences:
                    result.append(sent.text)
        if 'http://' in l or 'https://' in l:
            started = True
    f.close()
    return result

# rpath = 'original/test/raw/nord_stream_cs.txt_file_3.txt'
# parse_raw_file(rpath)


def merge_sents_and_ents(stanza_nlp, spacy_nlp, raw_file_path, annt_file_path):
    '''
    params:
    -----------------
    sents: ['this is a sentence.', 'another one?']
    ents: [(phrase1, type1), (phrase2, type2)]

    returns:
    -----------------
    tokenized and annotated sentences:
    [[(t1, annt1), (t2, annt2)], [(t3, annt3), (t4, annt4), (t5, annt5)]]
    '''

    def find_ent(sent, ents):
        result = {}
        for ent_text, ent_type in ents:
            if ent_text in sent:
                start = sent.index(ent_text)
                end = start + len(ent_text)
                result[(start, end)] = ent_type
        return result

    sents = parse_raw_file(raw_file_path, stanza_nlp)
    ents = parse_annt_file(annt_file_path)
    result = []
    for sent in sents:
        sent_arr = []
        _dict = find_ent(sent, ents)
        doc = spacy_nlp(sent)
        for t in doc:
            label = 'O'
            if len(_dict) > 0:
                for start, end in _dict.keys():
                    if t.idx >= start and t.idx < end:
                        head = 'B-' if t.idx == start else 'I-'
                        label = head + _dict[(start, end)]
                        break
            sent_arr.append((t.text, label))
        result.append(sent_arr)
    return result


def extract_ner_bio_sents(folder='test'):
    import os
    from tqdm import tqdm
    import stanza
    from spacy_stanza import StanzaLanguage
    snlp = stanza.Pipeline(lang="cs", logging_level='ERROR')
    nlp = StanzaLanguage(snlp)

    annt_path = os.path.join('original', folder, 'annotated')
    raw_path = os.path.join('original', folder, 'raw')
    annts = sorted(os.listdir(annt_path))
    annts = list(filter(lambda x: '.out' in x, annts))
    raws = sorted(os.listdir(raw_path))
    raws = list(filter(lambda x: '.txt' in x, raws))
    assert len(annts) == len(raws)

    results = []
    for a, r in tqdm(zip(annts, raws), total=len(raws)):
        aname = a.split('.')[0]
        rname = r.split('.')[0]
        assert aname == rname
        apath = os.path.join(annt_path, a)
        rpath = os.path.join(raw_path, r)
        results += merge_sents_and_ents(snlp, nlp, rpath, apath)
    return results


def write_ner_bio_file():
    def write_sents(file_name, sents):
        print(f'writing {len(sents)} sentences to {file_name}')
        f = open(file_name, 'w', encoding='utf8')
        for sent in sents:
            for token, label in sent:
                f.write(token + ' ' + label + '\n')
            f.write('\n')
        f.close()

    import random
    sents1 = extract_ner_bio_sents('test')
    sents2 = extract_ner_bio_sents('train')
    all_sents = sents1 + sents2
    random.shuffle(all_sents)
    total = len(sents1) + len(sents2)
    train_count = int(total * 0.75)
    dev_count = int(total * 0.10)
    train_sents = []
    dev_sents = []
    test_sents = []
    count = 0
    for sent in all_sents:
        if count < train_count:
            train_sents.append(sent)
        elif count < train_count + dev_count:
            dev_sents.append(sent)
        else:
            test_sents.append(sent)
        count += 1

    write_sents('all.txt', all_sents)
    write_sents('train.txt', train_sents)
    write_sents('test.txt', test_sents)
    write_sents('dev.txt', dev_sents)


if __name__ == '__main__':
    write_ner_bio_file()
