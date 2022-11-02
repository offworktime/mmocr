#!/usr/bin/env python
import os
import os.path as osp

import yaml

dataset_zoo_path = '../../dataset_zoo'
datasets = os.listdir(dataset_zoo_path)
datasets.sort()

table = '# Overview\n'
table += '## Supported Datasets\n'
table += '| Dataset Name | Text Detection | Text Recognition | Text Spotting | KIE |\n' \
         '|--------------|----------------|------------------|---------------|-----|\n'  # noqa: E501
details = '## Dataset Details\n'

for dataset in datasets:
    meta = yaml.safe_load(
        open(osp.join(dataset_zoo_path, dataset, 'metafile.yml')))
    dataset_name = meta['Name']
    paper = meta['Paper']
    data = meta['Data']

    table += '| [{}](#{}) | {} | {} | {} | {} |\n'.format(
        dataset,
        dataset_name.lower().replace(' ', '-'),
        '✓' if 'textdet' in data['Tasks'] else '',
        '✓' if 'textrecog' in data['Tasks'] else '',
        '✓' if 'textspotting' in data['Tasks'] else '',
        '✓' if 'kie' in data['Tasks'] else '',
    )

    details += '### {}\n'.format(dataset_name)
    details += "> \"{}\", *{}*, {}.\n\n".format(paper['Title'], paper['Venue'],
                                                paper['Year'])

    # Basic Info
    details += 'A. Basic Info\n'
    details += ' - Official Website: [{}]({})\n'.format(
        dataset, data['Website'])
    details += ' - Year: {}\n'.format(paper['Year'])
    details += ' - Language: {}\n'.format(data['Language'])
    details += ' - Scene: {}\n'.format(data['Scene'])
    details += ' - Annotation Granularity: {}\n'.format(data['Granularity'])
    details += ' - Supported Tasks: {}\n'.format(data['Tasks'])
    details += ' - License: [{}]({})\n'.format(data['License']['Type'],
                                               data['License']['Link'])

    # Format
    details += '<details> <summary>B. Annotation Format</summary>\n\n</br>'
    sample_path = osp.join(dataset_zoo_path, dataset, 'sample_anno.md')
    if osp.exists(sample_path):
        with open(sample_path, 'r') as f:
            samples = f.readlines()
            samples = ''.join(samples)
            details += samples
    details += '</details>\n\n</br>'

    # Reference
    details += 'C. Reference\n'
    details += '```bibtex\n{}\n```\n'.format(paper['BibTeX'])

datasetzoo = table + details

with open('user_guides/data_prepare/datasetzoo.md', 'w') as f:
    f.write(datasetzoo)
