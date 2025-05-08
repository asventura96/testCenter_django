# templatetags/custom_filters.py

"""
Este módulo contém filtros e tags personalizados para templates Django.
"""

from urllib.parse import urlencode, parse_qs

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def remove_page_param(query_params):
    """
    Remove o parâmetro 'page' dos query parameters.
    
    Args:
        query_params (str): Query parameters da URL.
    
    Returns:
        str: Query parameters sem o parâmetro 'page'.
    """
    params = parse_qs(query_params)
    params.pop('page', None)  # Remove o parâmetro 'page', se presente
    return urlencode(params, doseq=True)

@register.simple_tag
def render_search_fields(fields, request):
    """
    Gera dinamicamente os campos de pesquisa com base em um dicionário.
    
    Args:
        fields (list): Lista de dicionários contendo informações dos campos.
        request (HttpRequest): Objeto de requisição HTTP.
    
    Returns:
        str: HTML dos campos de pesquisa.
    
    Exemplo de uso no template:
    {% render_search_fields search_fields request %}
    """
    form_html = '<div class="apps-list-form-group-search">'
    for field in fields:
        field_name = field.get("name")
        field_label = field.get("label", field_name.capitalize())
        field_type = field.get("type", "text")
        field_options = field.get("options", [])

        value = request.GET.get(field_name, "")

        form_html += f"""
        <div class="apps-list-form-group-search-sub">
            <input type="checkbox" id="check-{field_name}" data-target="{field_name}">
            <label for="search-{field_name}">{field_label}:</label>
        """

        if field_type == "select":
            form_html += (
                f'<select name="{field_name}" id="{field_name}" '
                f'class="select-search select2">'
            )
            form_html += '<option value="">-- Selecione --</option>'
            for option_value, option_label in field_options:
                selected = 'selected' if str(value) == str(option_value) else ''
                form_html += f'<option value="{option_value}" {selected}>{option_label}</option>'
            form_html += '</select>'

        else:  # Campos de texto, padrão
            form_html += (
                f'<input type="{field_type}" id="{field_name}" name="{field_name}" '
                f'value="{value}" class="form-control">'
            )

        form_html += "</div>"

    form_html += "</div>"

    return mark_safe(form_html)

@register.filter
def get_item(dictionary, key):
    """
    Obtém um item de um dicionário pelo seu chave.
    
    Args:
        dictionary (dict): Dicionário de onde o item será obtido.
        key (str): Chave do item a ser obtido.
    
    Returns:
        any: Valor associado à chave no dicionário.
    """
    print(f"GET parameters: {dictionary}")
    print(f"Key being accessed: {key}")
    return dictionary.get(key)
