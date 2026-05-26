from flask import request

def generar_paginacion(limit, offset, request, total_items):
    base_url = request.base_url
    def generar_new_url(new_offset):
        args = request.args.copy()
        args['_limit'] = limit
        args['_offset'] = new_offset
        query_string = '&'.join([f"{key}={value}" for key, value in args.items()])
        return f"{base_url}?{query_string}"
    
    

    links = {
            }
    
    if offset > 0:
            links["prev"] = {"href": generar_new_url(max(0,offset - limit))}
            links["first"] = {"href": generar_new_url(0)}

    if offset + limit < total_items:
            links["next"] = {"href": generar_new_url(offset + limit)}
            
    if total_items > 0:
            last_offset = ((total_items - 1) // limit) * limit
            if offset < last_offset:
                links["last"] = {"href": generar_new_url(last_offset)}
        
    
    return links 



    
        
    