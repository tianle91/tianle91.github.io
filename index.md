[About](about.md)

[Projects](projects.md)

[Publications](publications.md)


# Blog
<ul>
  {% for post in site.posts %}
    {% if post.hidden != true %}
      <li>
        <a href="{{ post.url }}">{{ post.title }}</a>
      </li>
    {% endif %}
  {% endfor %}
</ul>
