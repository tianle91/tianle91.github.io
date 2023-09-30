[projects](projects.md)

[publications](publications.md)

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

# About
I consider these to be appropriate levels of sharing:
- How to pronounce [Tianle Chen](https://translate.google.com/#auto/en/%E9%99%88%E5%A4%A9%E4%B9%90)
- Reach me by [tianlechen@gmail.com](mailto:tianlechen@gmail.com)
- Corporate stuff on [linkedin](https://www.linkedin.com/in/tianlechen/)
- I share code on [github](https://github.com/tianle91)
- [I love trains](/assets/about/factorio.jpg)

[tianle91/tianle91.github.io](https://github.com/tianle91/tianle91.github.io)
