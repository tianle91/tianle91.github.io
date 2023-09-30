[About](/about.md)

# Blog
<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>

## New hire selected readings
<ul>
  {% for tag in site.tags %}
    {% if tag[0] == "newhire" %}
      {% for post in tag[1] %}
        <li>
          <a href="{{ post.url }}">{{ post.title }}</a>
        </li>
      {% endfor %}
    {% endif %}
  {% endfor %}
</ul>
