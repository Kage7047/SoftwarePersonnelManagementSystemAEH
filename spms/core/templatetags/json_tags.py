from django import template
from django.utils.safestring import mark_safe

register = template.Library()

def render_json_as_table(data):
    if isinstance(data, dict):
        rows = []
        for key, value in data.items():
            rows.append(
                f"<tr><th style='text-align:left; vertical-align:top; padding:6px; background:#f2f2f2;'>{key}</th>"
                f"<td style='padding:6px;'>{render_json_as_table(value)}</td></tr>"
            )
        return f"<table style='border-collapse:collapse; border:1px solid #ccc; width:100%; margin-bottom:10px;'>{''.join(rows)}</table>"
    elif isinstance(data, list):
        rows = []
        for i, item in enumerate(data):
            rows.append(
                f"<tr><th style='text-align:left; vertical-align:top; padding:6px; background:#f9f9f9;'>{i}</th>"
                f"<td style='padding:6px;'>{render_json_as_table(item)}</td></tr>"
            )
        return f"<table style='border-collapse:collapse; border:1px solid #ccc; width:100%; margin-bottom:10px;'>{''.join(rows)}</table>"
    else:
        return f"<span>{str(data)}</span>"

@register.simple_tag
def json_table(data):
    return mark_safe(render_json_as_table(data))
