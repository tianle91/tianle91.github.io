---
layout: default
title: Tianle Chen
nav_url: /
---
<section class="home-intro">
  <p class="eyebrow">Apps · Maps · Writing</p>
  <h1>Hi, I’m Tianle.</h1>
  <p>I build apps as tchdevs, explore data through interactive tools, and write about technology.</p>
</section>

<section aria-labelledby="apps-title">
  <div class="section-heading"><h2 id="apps-title">Apps by tchdevs</h2><a href="/apps/">Explore the apps →</a></div>
  <div class="home-apps">
    {% for app in site.data.apps %}{% if app.featured %}
    <article class="home-app">
      <img src="/assets/apps/{{ app.slug }}.jpg" width="64" height="64" alt="">
      <div><h3><a href="/apps/#{{ app.slug }}">{{ app.name }}</a></h3><p>{{ app.summary }}</p></div>
    </article>
    {% endif %}{% endfor %}
  </div>
</section>

<section id="interactive" aria-labelledby="interactive-title">
  <div class="section-heading"><h2 id="interactive-title">Interactive</h2><a href="/interactive/">All maps &amp; charts →</a></div>
  <div class="project-previews">
    <article class="project-preview">
      <a href="/StaticSites/us-canada-yield-curves/output/us-canada-yield-curves.html"><img src="/StaticSites/us-canada-yield-curves/tests/snapshots/desktop.jpg" width="720" height="405" alt="Preview of US and Canada government yield curves" loading="lazy"></a>
      <h3><a href="/StaticSites/us-canada-yield-curves/output/us-canada-yield-curves.html">US &amp; Canada yield curves</a></h3>
      <p>Compare government bond yields across maturities and historical dates.</p>
    </article>
    <article class="project-preview">
      <a href="/StaticSites/toronto-crime-map/output/toronto-crime-map.html"><img src="/StaticSites/toronto-crime-map/tests/snapshots/desktop.jpg" width="720" height="405" alt="Preview of Toronto reported crime by location" loading="lazy"></a>
      <h3><a href="/StaticSites/toronto-crime-map/output/toronto-crime-map.html">Toronto reported crime</a></h3>
      <p>Explore police-reported incidents by location and offence type.</p>
    </article>
  </div>
</section>

{% assign visible_posts = site.posts | where_exp: "post", "post.hidden == nil or post.hidden == false" %}
{% if visible_posts.size > 0 %}
<section id="blog" aria-labelledby="writing-title">
  <div class="section-heading"><h2 id="writing-title">Recent writing</h2><a href="/writing/">All writing →</a></div>
  <ul class="writing-list">
    {% for post in visible_posts limit:3 %}
    <li><time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: '%B %-d, %Y' }}</time><h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3></li>
    {% endfor %}
  </ul>
</section>
{% endif %}
