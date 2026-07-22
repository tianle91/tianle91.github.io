[About](about.md)

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


# Interactive

- [Union Station commute-shed](/StaticSites/union-station-transit-isochrone/output/union-station-transit-isochrone.html)
  — where you can reach Union by transit in 30 / 60 / 90 / 120 minutes.
- [Toronto services for vulnerable populations](/StaticSites/toronto-vulnerable-services-map/output/toronto-vulnerable-services-map.html)
  — shelters, warming & respite centres, drop-ins, harm reduction, housing supports.
- [Toronto DineSafe food-safety inspections](/StaticSites/toronto-dinesafe-map/output/toronto-dinesafe-map.html)
  — one pin per establishment, coloured by its latest outcome (Pass / Conditional Pass / Closed), searchable by name / type / address.
- [Ontario OHIP physiotherapy clinics](/StaticSites/ontario-physiotherapy-clinics-map/output/ontario-physiotherapy-clinics-map.html)
  — the 255 publicly-funded clinics and hospitals, searchable by name / city / postal code.
- [Margin debt vs. the S&P 500](/StaticSites/margin-sp500-m2-visualization/output/margin-sp500-m2-visualization.html)
  — FINRA margin debt against the S&P 500, M2, CPI and PPI, rebased to a chosen anchor date.

Source for all five: [github.com/tianle91/StaticSites](https://github.com/tianle91/StaticSites)


# Misc
467KkRS4G1ZLnvNLk83TZ3E2QZMUW37w4h5gKJNCKCA6Xmsx1rLKbezMU7N3mmHtJUC8o88HMWK6jYkBzMXsm9iq4hdVo6j
