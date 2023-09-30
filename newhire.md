<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GB6DWWMD6X"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-GB6DWWMD6X');
</script>

# New Hire Readings
{% for tag in site.tags %}
  {% if tag[0] == "newhire" %}
    <ul>
        {% for post in tag[1] %}
        <li><a href="{{ post.url }}">{{ post.title }}</a></li>
        {% endfor %}
    </ul>
  {% endif %}
{% endfor %}
