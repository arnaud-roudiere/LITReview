from django import template
from django.utils.safestring import mark_safe

register = template.Library()


register = template.Library()


@register.filter()
def addclass(value, class_name):
    return value.as_widget(attrs={"class": class_name})


@register.filter()
def addclassplaceholder(value, class_name):
    return value.as_widget(attrs={"class": class_name,
                                  "placeholder": value.label})


@register.filter
def model_type(value):
    return type(value).__name__


@register.filter()
def star(value):
    if value != 0:
        value = value * "\u2605"
        return f" - {value}"
    return ""


@register.simple_tag(takes_context=True)
def page_name(context, user, has_review):
    if context["user"] == user:
        if has_review:
            return "Ticket - Vous"
        return "Vous avez publié un ticket"
    return f"Ticket - {user}"


@register.filter(is_safe=True)
def convert_to_radio_btns(value):
    content = ""
    for i in range(6):
        print("ze", i)
        checked = ""
        if value == i:
            checked = "checked"
        content += (
            '<div><input type="radio" value="'
            + str(i)
            + '" name="rating" id="'
            + str(i)
            + '" '
            + checked
            + '> <label for="'
            + str(i)
            + '"> - '
            + str(i)
            + "</label></div>"
        )
    return mark_safe(content)


@register.filter
def del_modal_ticket_name(instance):
    return f'le ticket "{str(instance).__str__()}"'


@register.filter
def del_modal_review_name(instance):
    return f'votre commentaire "{str(instance).__str__()}"'
