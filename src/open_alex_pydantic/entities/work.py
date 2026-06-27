from __future__ import annotations

from typing import Optional
from pydantic import Field

from open_alex_pydantic.entities.base import BaseEntity

# ---------------------------------------------------------------------------
# Supporting models for Work
# ---------------------------------------------------------------------------


class WorkIds(BaseEntity):
    """External identifiers for a Work."""

    openalex: Optional[str] = None
    doi: Optional[str] = None
    mag: Optional[int] = None
    pmid: Optional[str] = None
    pmcid: Optional[str] = None


class WorkBiblio(BaseEntity):
    """Bibliographic information: volume, issue, first_page, last_page."""

    volume: Optional[str] = None
    issue: Optional[str] = None
    first_page: Optional[str] = None
    last_page: Optional[str] = None


class ApcInfo(BaseEntity):
    """Article Processing Charge information (used by apc_list and apc_paid)."""

    value: Optional[int] = None
    currency: Optional[str] = None
    value_usd: Optional[int] = None
    provenance: Optional[str] = None


class CitationNormalizedPercentile(BaseEntity):
    """Citation count percentile normalised by work type, year, and subfield."""

    value: Optional[float] = None
    is_in_top_1_percent: Optional[bool] = None
    is_in_top_10_percent: Optional[bool] = None


class CitedByPercentileYear(BaseEntity):
    """Percentile rank compared to other works published in the same year."""

    min: Optional[int] = None
    max: Optional[int] = None


class WorkCountByYear(BaseEntity):
    """Cited-by count for a specific year."""

    year: int
    cited_by_count: int


class WorkSustainableDevelopmentGoal(BaseEntity):
    """A UN Sustainable Development Goal with a relevance score for a Work."""

    id_: str = Field(alias="id")
    display_name: str
    score: float


class MeshTag(BaseEntity):
    """A MeSH (Medical Subject Headings) tag for a Work indexed in PubMed."""

    descriptor_ui: str
    descriptor_name: str
    qualifier_ui: Optional[str] = None
    qualifier_name: Optional[str] = None
    is_major_topic: bool


class HasContent(BaseEntity):
    """Availability of downloadable full-text content for a Work."""

    pdf: Optional[bool] = None
    grobid_xml: Optional[bool] = None


class DehydratedSource(BaseEntity):
    """Reduced-field Source used in nested contexts (e.g. inside a Location)."""

    id_: Optional[str] = Field(default=None, alias="id")
    display_name: Optional[str] = None
    issn_l: Optional[str] = None
    issn: Optional[list[str]] = None
    is_oa: Optional[bool] = None
    is_in_doaj: Optional[bool] = None
    is_core: Optional[bool] = None
    host_organization: Optional[str] = None
    host_organization_name: Optional[str] = None
    host_organization_lineage: Optional[list[str]] = None
    type_: Optional[str] = Field(default=None, alias="type")


class Location(BaseEntity):
    """A place where a Work is hosted."""

    is_oa: Optional[bool] = None
    landing_page_url: Optional[str] = None
    pdf_url: Optional[str] = None
    source: Optional[DehydratedSource] = None
    license_: Optional[str] = Field(default=None, alias="license")
    license_id: Optional[str] = None
    version: Optional[str] = None
    is_accepted: Optional[bool] = None
    is_published: Optional[bool] = None


class OpenAccess(BaseEntity):
    """Open access status information for a Work."""

    is_oa: Optional[bool] = None
    oa_status: Optional[str] = None
    oa_url: Optional[str] = None
    any_repository_has_fulltext: Optional[bool] = None


class DehydratedAuthor(BaseEntity):
    """Reduced-field Author used in nested contexts (e.g. inside Authorship)."""

    id_: Optional[str] = Field(default=None, alias="id")
    display_name: Optional[str] = None
    orcid: Optional[str] = None


class DehydratedInstitution(BaseEntity):
    """Reduced-field Institution used in nested contexts (e.g. inside Authorship)."""

    id_: Optional[str] = Field(default=None, alias="id")
    display_name: Optional[str] = None
    ror: Optional[str] = None
    country_code: Optional[str] = None
    type_: Optional[str] = Field(default=None, alias="type")
    lineage: Optional[list[str]] = None


class AuthorshipAffiliation(BaseEntity):
    """A raw affiliation string linked to resolved institution IDs."""

    raw_affiliation_string: Optional[str] = None
    institution_ids: Optional[list[str]] = None


class Authorship(BaseEntity):
    """An author and their institutional affiliations for a specific Work."""

    author_position: Optional[str] = None
    author: Optional[DehydratedAuthor] = None
    institutions: Optional[list[DehydratedInstitution]] = None
    countries: Optional[list[str]] = None
    is_corresponding: Optional[bool] = None
    raw_author_name: Optional[str] = None
    raw_affiliation_strings: Optional[list[str]] = None
    affiliations: Optional[list[AuthorshipAffiliation]] = None


class TopicHierarchyEntry(BaseEntity):
    """A reference to an item in the topic hierarchy (subfield, field, or domain)."""

    id_: Optional[str] = Field(default=None, alias="id")
    display_name: Optional[str] = None


class WorkTopic(BaseEntity):
    """A topic assigned to a Work with a relevance score and hierarchy context."""

    id_: Optional[str] = Field(default=None, alias="id")
    display_name: Optional[str] = None
    score: Optional[float] = None
    subfield: Optional[TopicHierarchyEntry] = None
    field: Optional[TopicHierarchyEntry] = None
    domain: Optional[TopicHierarchyEntry] = None


class WorkKeyword(BaseEntity):
    """A keyword associated with a Work, derived from its topics."""

    id_: Optional[str] = Field(default=None, alias="id")
    display_name: Optional[str] = None
    score: Optional[float] = None


class DehydratedFunder(BaseEntity):
    """Reduced-field Funder used in nested contexts (e.g. inside a Work)."""

    id_: Optional[str] = Field(default=None, alias="id")
    display_name: Optional[str] = None
    ror: Optional[str] = None


class WorkAward(BaseEntity):
    """A dehydrated funding award linked to a Work."""

    id_: Optional[str] = Field(default=None, alias="id")
    display_name: Optional[str] = None
    funder_award_id: Optional[str] = None
    funder_id: Optional[str] = None
    funder_display_name: Optional[str] = None
    doi: Optional[str] = None


class WorkConcept(BaseEntity):
    """A legacy concept tag assigned to a Work (deprecated — use topics instead)."""

    id_: Optional[str] = Field(default=None, alias="id")
    wikidata: Optional[str] = None
    display_name: Optional[str] = None
    level: Optional[int] = None
    score: Optional[float] = None


# ---------------------------------------------------------------------------
# Main Work model
# ---------------------------------------------------------------------------


class Work(BaseEntity):
    """A scholarly document (article, book, dataset, thesis, etc.) in OpenAlex."""

    id_: Optional[str] = Field(default=None, alias="id")
    doi: Optional[str] = None
    title: Optional[str] = None
    display_name: Optional[str] = None
    publication_year: Optional[int] = None
    publication_date: Optional[str] = None
    type_: Optional[str] = Field(default=None, alias="type")
    language: Optional[str] = None
    cited_by_count: Optional[int] = None
    is_retracted: Optional[bool] = None
    is_paratext: Optional[bool] = None
    primary_location: Optional[Location] = None
    locations: Optional[list[Location]] = None
    locations_count: Optional[int] = None
    best_oa_location: Optional[Location] = None
    open_access: Optional[OpenAccess] = None
    authorships: Optional[list[Authorship]] = None
    ids: Optional[WorkIds] = None
    biblio: Optional[WorkBiblio] = None
    # Maps each word to a list of character positions in the abstract.
    abstract_inverted_index: Optional[dict[str, list[int]]] = None
    referenced_works: Optional[list[str]] = None
    referenced_works_count: Optional[int] = None
    related_works: Optional[list[str]] = None
    topics: Optional[list[WorkTopic]] = None
    primary_topic: Optional[WorkTopic] = None
    keywords: Optional[list[WorkKeyword]] = None
    funders: Optional[list[DehydratedFunder]] = None
    awards: Optional[list[WorkAward]] = None
    apc_list: Optional[ApcInfo] = None
    apc_paid: Optional[ApcInfo] = None
    fwci: Optional[float] = None
    citation_normalized_percentile: Optional[CitationNormalizedPercentile] = None
    cited_by_percentile_year: Optional[CitedByPercentileYear] = None
    counts_by_year: Optional[list[WorkCountByYear]] = None
    sustainable_development_goals: Optional[list[WorkSustainableDevelopmentGoal]] = None
    mesh: Optional[list[MeshTag]] = None
    indexed_in: Optional[list[str]] = None
    has_content: Optional[HasContent] = None
    content_url: Optional[str] = None
    fulltext_origin: Optional[str] = None
    best_open_version: Optional[str] = None
    cited_by_api_url: Optional[str] = None
    created_date: Optional[str] = None
    updated_date: Optional[str] = None
    # Deprecated field — use topics instead
    concepts: Optional[list[WorkConcept]] = None
