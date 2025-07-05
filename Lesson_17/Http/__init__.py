import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger function received a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            req_body = {}
        name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Xin chào, {name}!")
    else:
        return func.HttpResponse(
            "Vui lòng cung cấp tên trong query string hoặc body.",
            status_code=400
        )
