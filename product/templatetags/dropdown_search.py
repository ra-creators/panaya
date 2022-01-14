from django import template

register = template.Library()

dropdown_template = '''
    <select name="category" value="#{formdata.category}" class="form-select"
        aria-label="Category select">
        <option value="0" {% if '' == formdata.category %}selected="selected" {% endif %}>
            category all</option>
        {% for categorie in categories %}
        {% if categorie.id|stringformat:"i" == formdata.category %}
        <option value="#{categorie.id}" data-bool="yes" data-cat=#{categorie.id}
            data-form=#{formdata.category} selected="selected">
            #{categorie}
        </option>
        {% else %}
        <option value="#{categorie.id}" data-bool="no" data-cat=#{categorie.id}
            data-form=#{formdata.category}>
            #{categorie}
        </option>
        {% endif %}
        {% endfor %}
    </select>'''


def render(objects, fromdata):
    pass
