from urllib.parse import urlparse
from typing import Optional

from loguru import logger
from tqdm import tqdm
from typing_extensions import Annotated
from zenml import get_step_context, step

from gallery_recommender.application.crawlers.dispatcher import CrawlerDispatcher
# from gallery_recommender.application.crawlers.googledocs import GoogleDocsReflectionsCrawler



@step
def crawl_links(links: list[str], reflections: bool = False, _after_delete: bool = None) -> Annotated[list[str], "crawled_links"]:
    # register the crawlers
    dispatcher = CrawlerDispatcher.build().register_google_docs()

    logger.info(f"Crawling {len(links)} links...")

    metadata = {}
    successful_crawls = 0
    added_galleries = 0
    added_exhibitions = 0
    added_reflections = 0

    if reflections:
        for link in tqdm(links, desc="Crawling links..."):
            successful_crawl, crawled_domain, _, added_reflections = _crawl_link(dispatcher, link, reflections)
            successful_crawls += successful_crawl
            added_reflections += added_reflections


        metadata = _add_to_metadata(metadata, crawled_domain, successful_crawl, added_galleries, added_exhibitions)

        step_context = get_step_context()
        step_context.add_output_metadata(
        output_name="crawled_links",
        metadata=metadata
        )

        logger.info(f"Successfully crawled {successful_crawls} out of {len(links)} links")
        logger.info(f"Added {added_reflections} reflections")
        
    else:
        for link in tqdm(links, desc="Crawling links..."):
            successful_crawl, crawled_domain, added_galleries, added_exhibitions = _crawl_link(dispatcher, link, reflections)
            successful_crawls += successful_crawl
            added_galleries += added_galleries
            added_exhibitions += added_exhibitions

        metadata = _add_to_metadata(metadata, crawled_domain, successful_crawl, added_galleries, added_exhibitions)

        step_context = get_step_context()
        step_context.add_output_metadata(
        output_name="crawled_links",
        metadata=metadata
        )

        logger.info(f"Successfully crawled {successful_crawls} out of {len(links)} links")
        logger.info(f"Added {added_galleries} galleries and {added_exhibitions} exhibitions")

    return links


def _crawl_link(dispatcher: CrawlerDispatcher,link: str, reflections: bool = False) -> tuple[bool, str, Optional[int], int]:
    # if reflections is true, use the GoogleDocsReflectionsCrawler
    if reflections: 
        crawler = GoogleDocsReflectionsCrawler()
        crawler_domain = urlparse(link).netloc
        try:
            added_reflections = crawler.extract(link=link)

            return (True, crawler_domain, None, added_reflections)
        
        except Exception as e:
            logger.error(f"An error occurred while crawling: {e!s}")
            return (False, crawler_domain, 0, 0)
        
    else:
        crawler = dispatcher.get_crawler(link)
        crawler_domain = urlparse(link).netloc

        try:
            added_galleries, added_exhibitions = crawler.extract(link=link)

            return (True, crawler_domain, added_galleries, added_exhibitions)
        
        except Exception as e:
            # logger.error(f"Error crawling link: {link} using {crawler}")
            logger.error(f"An error occurred while crawling: {e!s}")
            return (False, crawler_domain, 0, 0)
        

def _add_to_metadata(metadata: dict, domain: str, successful_crawl: bool, added_galleries: int, added_exhibitions: int) -> dict:
    if domain not in metadata:
        metadata[domain] = {}
    metadata[domain]["successful"] = metadata.get(domain, {}).get("successful", 0) + successful_crawl
    metadata[domain]["total"] = metadata.get(domain, {}).get("total", 0) + 1
    metadata[domain]["added galleries"] = metadata.get(domain, {}).get("added galleries", 0) + added_galleries
    metadata[domain]["added exhibitions"] = metadata.get(domain, {}).get("added exhibitions", 0) + added_exhibitions

    return metadata

    