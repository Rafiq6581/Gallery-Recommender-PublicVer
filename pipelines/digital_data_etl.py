from zenml import pipeline

from steps.etl import crawl_links, delete_data


@pipeline
def digital_data_etl(collection_names: list[str], links: list[str], reflections: bool = False) -> str:
    delete_status = delete_data(collection_names)
    last_step = crawl_links(links, reflections=reflections, _after_delete=delete_status)

    return last_step.invocation_id


