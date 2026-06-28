from __future__ import annotations

from typing import Optional

from pydantic import Field

from open_alex_pydantic.entities.base import BaseEntity


class AuthorIds(BaseEntity):
    """External identifiers for an Author."""

    openalex: Optional[str] = None
    orcid: Optional[str] = None


class Institution(BaseEntity):
    """An institution entity (used for both affiliation and last_known_institutions)."""

    id_: str = Field(alias="id")
    ror: Optional[str] = None
    display_name: Optional[str] = None
    type_: Optional[str] = Field(default=None, alias="type")
    country_code: Optional[str] = None
    lineage: Optional[list[str]] = None


class Affiliation(BaseEntity):
    """An affiliation of an author to an institution."""

    id_: Optional[str] = Field(default=None, alias="id")
    ror: Optional[str] = None
    type_: Optional[str] = Field(default=None, alias="type")
    country_code: Optional[str] = None
    lineage: Optional[list[str]] = None
    institution: Optional[Institution] = None
    years: Optional[list[int]] = None


class LastKnownInstitution(BaseEntity):
    """A last known institution of an author."""

    id_: str = Field(alias="id")
    ror: Optional[str] = None
    type_: Optional[str] = Field(default=None, alias="type")
    country_code: Optional[str] = None
    lineage: Optional[list[str]] = None
    continent: Optional[str] = None
    is_global_south: Optional[bool] = None


class SummaryStats(BaseEntity):
    """Summary statistics for an author's publication metrics."""

    h_index: Optional[int] = None
    i10_index: Optional[int] = None
    two_year_mean_citedness: Optional[float] = Field(
        default=None, alias="2yr_mean_citedness"
    )


class Topic(BaseEntity):
    """A topic classification for an author."""

    id_: str = Field(alias="id")
    display_name: Optional[str] = None
    count: Optional[int] = None
    subfield: Optional[TopicHierarchyEntry] = None
    field: Optional[TopicHierarchyEntry] = None
    domain: Optional[TopicHierarchyEntry] = None


class TopicHierarchyEntry(BaseEntity):
    """A reference to an item in the topic hierarchy (subfield, field, or domain)."""

    id_: str = Field(alias="id")
    display_name: Optional[str] = None


class XConceptsEntry(BaseEntity):
    """A concept entry from x-headers for an author."""

    id_: str = Field(alias="id")
    wikidata: Optional[str] = None
    display_name: Optional[str] = None
    score: Optional[float] = None


class CountsByYearEntry(BaseEntity):
    """Counts by year for an author's publications."""

    year: int
    works_count: Optional[int] = None
    oa_works_count: Optional[int] = None
    cited_by_count: Optional[int] = None


class Author(BaseEntity):
    """An author in the OpenAlex corpus."""

    id_: str = Field(alias="id")
    display_name: str
    orcid: Optional[str] = None
    scopus: Optional[str] = None
    works_count: Optional[int] = None
    cited_by_count: Optional[int] = None
    summary_stats: Optional[SummaryStats] = None
    affiliations: Optional[list[Affiliation]] = None
    last_known_institutions: Optional[list[LastKnownInstitution]] = None
    parsed_longest_name: Optional[str] = None
    x_concepts: Optional[list[XConceptsEntry]] = None
    topics: Optional[list[Topic]] = None
    ids: Optional[AuthorIds] = None
    block_key: Optional[str] = None
