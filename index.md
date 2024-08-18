[About](about.md)

[Projects](projects.md)

[Publications](publications.md)


# Blog
<ul>
  {% for post in site.posts %}
    {% if post.hidden == null or post.hidden == false %}
      <li>
        <a href="{{ post.url }}">{{ post.title }}</a>
        {{ post.excerpt }}
      </li>
    {% endif %}
  {% endfor %}
</ul>
