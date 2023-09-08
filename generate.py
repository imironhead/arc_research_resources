"""Utilities of generating research topic pages.

For example, the "Video Super Resolution" materals should be summaried in
./pages/vsr/README.md. It shuld look like:

---BEGIN ./pages/vsr/README.md
# Video Super Resolution

## Contents

- [Tags](#tags)
- [Research Papers](#research-papers)

## Tags

### Journals

#CVPR #ICCV #TOG

### Years

#Y2023 #Y2021 #Y2020

### Research Areas

#gan #temporal_coherence #video_compression #video_frame_interpolation
#video_frame_interpolation #video_super_resolution #video_super_resolution

## Research Papers

### Y2023

- [Paper 0](../../research_papers/paper_0_hash/)
    - One sentence summary of paper 0.
    - #CVPR #Y2023 #video_frame_interpolation

### Y2021

- [Paper 1](../../research_papers/paper_1_hash/)
    - One sentence summary of paper 1.
    - #ICCV #Y2021 #video_frame_interpolation

- [Paper 2](../../research_papers/paper_2_hash/)
    - One sentence summary of paper 2.
    - #ICCV #Y2021 #video_compression #video_super_resolution

### Y2020

- [Paper 3](../../research_papers/paper_3_hash/)
    - One sentence summary of paper 3.
    - #TOG #Y2020 #gan #temporal_coherence #video_super_resolution
---END ./pages/vsr/README.md

All the contents will be generated base on existing notes within
./research_papers/. Each note is expected to be a GitHub README.md within a
directory. For example, the note for the paper "Learning Temporal Coherence via
Self-Supervision for GAN-based Video Generation" is in
 ./research_papers/ltcsgvg/README.md.

Each note should follow the template:

---BEGIN template
# Paper Title

## OSS

One sentence summary of the paper.

## TAGs

#journal_tag #year_tag #topic_tag_0 #topic_tag_1 #topic_tag_etc

## The Rest of the other note
---END template

"""
import collections
import dataclasses
import glob
import itertools
import os
import typing


@dataclasses.dataclass
class Page:
    """General markdown page.

    Attributes:
        path: The path of the page README.md.
        title: The title of the page.
    """
    path: str
    title: str


class NotePageReader(Page):
    """Note reader.

    A note is a GitHub README.md with three blocks:
    - # Note Title
        - H1. The note title is extracted from this heading.
    - ## OSS
        - H2. The one-sentence-summary is extracted from the text under this
          heading.
    - ## TAGs
        - H2. The tags are extracted from the text under this heading.

    Attributes:
        one_sentence_summary: The one sentence summary in '## OSS' of the
            markdown.
        tags: The tags in '## TAGs' of the markdown.
        journal_tag: The tag of the paper journal. For example, '#CVPR'.
        year_tag: The tag of the paper publishing year. For example, '#Y2023'.
    """

    # List of known journal tags. Each NotePageReader should has exactly one
    # journal tag. The script sorts the tags and always put the journal tag in
    # the beginning of the tags.
    JOURNAL_TAGS = {
        '#AAAI', '#ARXIV', '#CVPR', '#ECCV', '#ICCV', '#IJCV', '#NOSSDAV', '#TOG',
    }

    @staticmethod
    def is_year_tag(tag: str) -> bool:
        """Checks if a string is a year tag.

        A year tag is a string starts with '#Y' and followed by 4 digits.

        Args:
            tag: A possible year tag string.
        """
        return len(tag) == 6 and tag[1] == 'Y' and tag[2:].isdigit()

    @staticmethod
    def is_journal_tag(tag: str) -> bool:
        """Checks if a string is a journal tag.

        A journal tag is one of the sting in NotePageReader.JOURNAL_TAGS.

        Args:
            tag: A possible journal tag string.
        """
        return tag in NotePageReader.JOURNAL_TAGS

    @staticmethod
    def collect_note_pages(root_path: str) -> list[typing.Self]:
        """Reads notes in the root_path and returns a list of NotePageReaders.

        Each note is expected to be a README.md within a directory in root_path.

        Args:
            root_path: The path to read page notes from.
        """
        return [
            NotePageReader(path)
            for path in glob.glob(os.path.join(root_path, '**/'))
        ]

    def __init__(self, path: str) -> None:
        """Initializes the note page.

        Title, one-sentence-summary and tags are extracted from the README.md
        file. Tags are also rearranged so the first one is always a journal tag
        while the second one is always a year tag.

        Args:
            path: The path to a directory that contains a README.md file.
        """
        note_title = ''
        note_one_sentence_summary = ''
        note_tags = []

        # NOTE: Reads markdown with built-in functions to prevent installing
        # extra packages.
        with open(os.path.join(path, 'README.md'), 'r') as file:
            # Removes the trailing newlines ('\n').
            lines = filter(lambda line: line.strip(), file)

            for line_0, line_1 in itertools.pairwise(lines):
                match line_0, line_1:
                    case (title, _) if title.startswith('# '):
                        note_title = title[2:].strip()
                    case (name, oss) if name.startswith('## OSS'):
                        note_one_sentence_summary = oss.strip()
                    case (name, tags) if name.startswith('## TAGs'):
                        note_tags = [
                            tag
                            for tag in tags.strip().split()
                            if tag.startswith('#')
                        ]

        if not all([note_title, note_one_sentence_summary, note_tags]):
            raise ValueError(
                f'Invalid note: {path}. Check path, title, oss or tags.')

        for idx in range(len(note_tags)):
            if NotePageReader.is_journal_tag(note_tags[idx]):
                note_tags[0], note_tags[idx] = note_tags[idx], note_tags[0]
            elif NotePageReader.is_year_tag(note_tags[idx]):
                note_tags[1], note_tags[idx] = note_tags[idx], note_tags[1]

        if len(note_tags) < 2:
            raise ValueError(
                f'Invalid note: {path}. A Note needs journal and year tags.')

        if not NotePageReader.is_journal_tag(note_tags[0]):
            raise ValueError(
                f'Invalid note: {path}. A Note needs a journal tag.')
        
        if not NotePageReader.is_year_tag(note_tags[1]):
            raise ValueError(f'Invalid note: {path}. A note needs a year tag.')

        super().__init__(path, note_title)

        self._one_sentence_summary = note_one_sentence_summary
        self._tags = note_tags[:2] + sorted(note_tags[2:])
    
    @property
    def one_sentence_summary(self) -> str:
        """Returns the one-sentence-summary extracted from README.md."""
        return self._one_sentence_summary
    
    @property
    def tags(self) -> list[str]:
        """Returns tags extracted from README.md."""
        return self._tags.copy()

    @property
    def journal_tag(self) -> str:
        """Returns the journal tag extracted from README.md."""
        return self._tags[0]
    
    @property
    def year_tag(self) -> str:
        """Returns the year tag extracted from README.md."""
        return self._tags[1]


class TopicPageWriter(Page):
    """Topic summary (e.g. VSR resources) writer.

    A topic page is a GitHub README.md markdown composed with several blocks.
    Currenntly, tag-block builder and note-collection-block builder are
    implemented.

    TODO: Implement dataset-collection-block to list all datasets related to
    the topic (note pages with tag #dataset).
    """

    def __init__(
            self,
            path: str,
            title: str,
            notes: typing.Iterable[NotePageReader]) -> None:
        """Initializes the empty topic page.

        Args:
            path: The directory for saving the README.md of this page.
            title: The title of this topic page.
            notes: The material for building blcoks for this topic page.
        """
        super().__init__(path, title)

        self._notes = list(notes) or []
        self._page_blocks = []

    def add_title_block(self) -> None:
        """Adds one line title block to the note page.

        The title should be placed in the beginning of the page. This function
        is just to make the implementation looks more general.
        """
        self._page_blocks.append([
            f'# {self.title}',
            '',
        ])

    def add_heading_block(self) -> None:
        """Adds a heading block to the note page.

        A heading block contains shortcuts to the other blocks. Because the
        writer does not know how many blocks will be appended later, this
        function adds a placeholder instead.

        The real heading block content will be build before saving to a markdown
        file.
        """
        self._page_blocks.append([
            '<<<HEADING BLOCK>>>',
            '',
        ])

    def add_note_collection_block(self) -> None:
        """Adds a note collection block to the note page.

        A note collection block contains a list of note group by the year tags.
        The note title, one-sentence-summary and tags are listed for each nore.
        For example,

        - [Learning Temporal Coherence via Self-Supervision for GAN-based Video Generation](../../research_papers/ltcsgvg/)
            - Proposed a spatio-temporal discriminator for temporal coherence of video generation.
            - #TOG #Y2020 #gan #temporal_coherence #video_super_resolution
        """
        block = [
            '## Research Papers',
            '',
        ]

        year_to_notes = collections.defaultdict(list)

        for note in self._notes:
            year_to_notes[note.year_tag[1:]].append(note)

        for year in sorted(year_to_notes.keys(), reverse=True):
            block.extend([
                f'### {year}',
                '',
            ])

            for note in year_to_notes[year]:
                note_relative_path = os.path.relpath(note.path, self.path)
                # NOTE: I want the trailing slash.
                note_relative_path = os.path.join(note_relative_path, '')

                block.extend([
                    f'- [{note.title}]({note_relative_path})',
                    f'    - {note.one_sentence_summary}',
                    f'    - {" ".join(note.tags)}',
                    '',
                ])

        self._page_blocks.append(block)

    def add_tag_collection_block(self) -> None:
        """Adds a tag collection block to the note page.

        A tag collection block contains a list of tags. Those tags are the union
        of tags of all notes.

        Tags are separated into three groups: journal tags, year tags and
        research area tags.
        """
        journal_tags = {note.journal_tag for note in self._notes}

        # Also build the shortcuts to notes of each year.
        year_tags = {
            f'[{note.year_tag}]({note.year_tag.lower()})'
            for note in self._notes
        }

        area_tags = itertools.chain.from_iterable(n.tags for n in self._notes)
        area_tags = itertools.filterfalse(
            NotePageReader.is_journal_tag, area_tags)
        area_tags = itertools.filterfalse(
            NotePageReader.is_year_tag, area_tags)
        area_tags = list(set(area_tags))

        journal_tags = ' '.join(sorted(journal_tags))
        year_tags = ' '.join(sorted(year_tags, reverse=True))
        area_tags = ' '.join(sorted(area_tags))

        self._page_blocks.append([
            '## Tags',
            '',
            '### Journals',
            '',
            journal_tags,
            '',
            '### Years',
            '',
            year_tags,
            '',
            '### Research Areas',
            '',
            area_tags,
            '',
        ])

    def save(self) -> None:
        """Saves all blocks into a GitHub markdown README.md."""
        blocks = []
        headings = None

        for block in self._page_blocks:
            match block:
                case ['<<<HEADING BLOCK>>>', *_]:
                    headings = [
                        '## Contents',
                        '',
                        '',
                    ]

                    blocks.append(headings)
                case [heading, *_]:
                    if headings:
                        heading_text = heading.replace('#', '').strip()
                        heading_link = heading_text.lower().replace(' ', '-')

                        headings.pop()
                        headings.extend([
                            f'- [{heading_text}](#{heading_link})',
                            '',
                        ])

                    blocks.append(block)

        os.makedirs(self.path, exist_ok=True)

        with open(os.path.join(self.path, 'README.md'), 'w') as output:
            lines = itertools.chain.from_iterable(blocks)

            output.write('\n'.join(lines))


class ResearchTopicPageWriter(TopicPageWriter):
    """Research topic summary page writer.

    The writer first filters note by their tags, then saves the page in a
    pre-defined format. All research topic page writers should inherit from this
    implementation to maintain consistent style.
    """

    def __init__(
            self,
            path: str,
            title: str,
            notes: typing.Iterable[NotePageReader],
            tags: typing.Iterable[str]) -> None:
        """Initializes the research topice page writer.

        Args:
            path: The path of a directory for saving the README.md.
            title: The title of this research topic, e.g. RecSys.
            notes: A collection of notes. The writer will build blocks base on
                the filtered notes.
            tags: A collection of tags. Notes without any of those tags are
                ignored.
        """
        area_tags = set(tags)

        notes  = [note for note in notes if set(note.tags) & area_tags]

        super().__init__(path, title, notes)

    def save(self) -> typing.Self:
        """Saves pre-defined blocks into a GitHub markdown README.md."""
        self.add_title_block()
        self.add_heading_block()
        self.add_tag_collection_block()
        self.add_note_collection_block()

        super().save()


class VSRTopicPageWriter(ResearchTopicPageWriter):
    """Video super resolution summary page writer."""

    def __init__(
            self,
            path: str,
            title: str,
            notes: typing.Iterable[NotePageReader]) -> None:
        """Initializes the Video Super Resolution research topice page writer.

        Args:
            path: The path of a directory for saving the README.md.
            title: The title of this research topic, e.g. RecSys.
            notes: A collection of notes. The writer will build blocks base on
                the filtered notes.
        """
        # NOTE:
        # Spatial super resolution: Super resolution.
        # Temporal super resolution: Video frame interpolation.
        # Spectrum super resolution: High dynamic range.
        area_tags = {
            '#360_video_streaming',
            '#high_dynamic_range_image', '#high_dynamic_range_video',
            '#single_image_super_resolution',
            '#video_denosing',
            '#video_frame_interpolation', '#video_super_resolution',
        }

        super().__init__(path, title, notes, area_tags)


class MainPage(Page):
    """Repository entry page writer.

    This page serves as the entry of the other research topic pages.
    """

    def __init__(self, path: str, title: str) -> None:
        """Initializes the main page writer.

        Args:
            path: The path of a directory for saving the README.md.
            title: The title of this research topic.
        """
        super().__init__(path, title)

        self._lines = [
            f'# {self.title}',
            '',
        ]

    def add_topic_page(self, path: str, title: str) -> None:
        """Adds one topic page to the list."""
        page_relative_path = os.path.relpath(path, self.path)

        # FIXME:
        page_relative_path = './' + page_relative_path + '/'

        self._lines.append(f'- [{title}]({page_relative_path})')

    def save(self) -> None:
        """Saves the entry page into a GitHub markdown README.md."""
        with open(os.path.join(self.path, 'README.md'), 'w') as output:
            output.write('\n'.join(self._lines))


def main() -> None:
    """Generates main page and research topic pages."""
    notes = NotePageReader.collect_note_pages('./research_papers/')

    topic_pages = [
        VSRTopicPageWriter('./pages/vsr/', 'Video Super Resolution', notes),
    ]

    main_page = MainPage('.', 'Research Topics')

    for topic_page in topic_pages:
        topic_page.save()

        main_page.add_topic_page(topic_page.path, topic_page.title)

    main_page.save()


if __name__ == '__main__':
    main()
