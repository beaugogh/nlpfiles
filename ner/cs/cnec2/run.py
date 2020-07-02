# parse the treex into sentences with tokens with entity types
import xml.etree.ElementTree as ET
import os
from tqdm import tqdm


class Sentence:
    def __init__(self, _id):
        self.id = _id
        self.tokens = []


class Token:
    def __init__(self, _id, text):
        self.id = _id
        self.text = text
        self.ent_type = 'O'


def update_token_ent_type(sentence, token_id, ent_type):
    for token in sentence.tokens:
        if token.id == token_id:
            token.ent_type = ent_type
            return token

    raise Exception(f'cannot find token with id {token_id}')


def parse_entity(sentence, e):
    ent_type = e[0].text
    arfs = e[2]
    if len(arfs) == 1:
        token_id = arfs.text
        update_token_ent_type(sentence, token_id, 'B' + '-' + ent_type)
    else:
        for i, arf in enumerate(arfs):
            token_id = arf.text
            head = 'B' if i == 0 else 'I'
            update_token_ent_type(sentence, token_id, head + '-' + ent_type)


def map_ent_type(name, fully_mapped):
    # map the entity type to the "regular four" categories
    # see original/doc/ner-type-hierarchy.pdf
    # if fully_mapped is true, map every ner type
    # if fully_mapped is false, discard number and time expression types
    if name in ['MISC', 'PER', 'ORG', 'LOC']:
        return name

    first = name[0].lower()
    if fully_mapped:
        if first in ['a', 'n', 'o', 't']:
            return 'MISC'
        elif first == 'g':
            return 'LOC'
        elif first in ['i', 'm']:
            return 'ORG'
        elif first == 'p':
            return 'PER'
        else:
            return 'MISC'
    else:
        numbers_and_times = ['a', 'n', 't']
        if first == 'g':
            return 'LOC'
        elif first in ['i', 'm']:
            return 'ORG'
        elif first == 'p':
            return 'PER'
        elif first in numbers_and_times:
            return 'O'
        else:
            return 'MISC'


def extract_sentences(treex_path, fully_mapped):
    tree = ET.parse(treex_path)
    root = tree.getroot()
    bundles = root[2]

    sentences = []
    for sent in tqdm(bundles):
        assert len(sent) == 1
        zones = sent[0]
        assert len(zones) == 1
        zone = zones[0]
        lang = zone.attrib['language']
        assert lang == 'cs'
        assert len(zone) == 1
        trees = zone[0]
        assert len(trees) == 2
        atree = trees[0]
        assert len(atree) == 2
        tokens = atree[1]
        # print(sent.attrib)
        sentence = Sentence(sent.attrib['id'])
        for t in tokens:
            tid = t.attrib['id']
            assert len(t) == 4
            ttext = t[0].text
            # print(tid, ttext)
            token = Token(tid, ttext)
            sentence.tokens.append(token)

        ntree = trees[1]
        assert len(ntree) <= 1
        if len(ntree) > 0:
            ents = ntree[0]
            if 'ne_type' in ents[0].tag:
                parse_entity(sentence, ents)
            elif 'LM' in ents[0].tag:
                for ent in ents:
                    parse_entity(sentence, ent)
            else:
                raise Exception('sth went wrong')

        sentences.append(sentence)

    # check the entity type distribution before vs after
    ent_dict = {}
    for sent in sentences:
        for t in sent.tokens:
            ent_type = t.ent_type.split('-')[1] if t.ent_type != 'O' else 'O'
            if ent_type in ent_dict:
                ent_dict[ent_type] = ent_dict[ent_type] + 1
            else:
                ent_dict[ent_type] = 1
    print('before: ', ent_dict)

    ent_dict = {}
    for sent in sentences:
        for t in sent.tokens:
            ent_type = t.ent_type.split('-')[1] if t.ent_type != 'O' else 'O'
            head = t.ent_type.split('-')[0] if t.ent_type != 'O' else None
            ent_type = map_ent_type(ent_type, fully_mapped) if ent_type != 'O' else 'O'
            if ent_type in ent_dict:
                ent_dict[ent_type] = ent_dict[ent_type] + 1
            else:
                ent_dict[ent_type] = 1
            t.ent_type = ent_type if head is None or ent_type == 'O' else head + '-' + ent_type

    print('after:', ent_dict)

    return sentences


def write_to_ner_bio_file(mode='test', fully_mapped=False):
    # candidate treex files:
    name_switch = {
        'test': 'named_ent_etest.treex',
        'dev': 'named_ent_dtest.treex',
        'train': 'named_ent_train.treex'
    }
    treex_file = name_switch[mode] if mode in name_switch else None
    if treex_file is not None:
        treex_folder = os.path.join('original', 'data', 'treex')
        treex_path = os.path.join(treex_folder, treex_file)
        sentences = extract_sentences(treex_path, fully_mapped)
        output_path = f'{mode}.txt'
        w = open(output_path, 'w', encoding='utf8')
        for sent in sentences:
            for t in sent.tokens:
                w.write(t.text + ' ' + t.ent_type + '\n')
            w.write('\n')
        w.close()
    else:
        raise Exception('mode should be "test", "dev", or "train"...')


if __name__ == "__main__":
    write_to_ner_bio_file('test', fully_mapped=False)
    write_to_ner_bio_file('dev', fully_mapped=False)
    write_to_ner_bio_file('train', fully_mapped=False)
