{{ fullname }}
{{ underline }}


..  automodule:: {{ fullname }}

{% block summary %}
{% if classes or functions or exceptions %}

{% block classes_summary %}
{% if classes %}
.. rubric:: Classes

.. autosummary::
{% for item in classes %}
  {{ item }}
{%- endfor %}
{% endif %}
{% endblock %}

{% block functions_summary %}
{% if functions %}
.. rubric:: Functions

.. autosummary::
{% for item in functions %}
  {{ item }}
{%- endfor %}
{% endif %}
{% endblock %}

{% block exceptions_summary %}
{% if exceptions %}
.. rubric:: Exceptions

.. autosummary::
{% for item in exceptions %}
  {{ item }}
{%- endfor %}
{% endif %}
{% endblock %}

{% endif %}
{% endblock %}


{% block class_details %}
{% if classes %}
{% for item in classes %}
{{ item }}
--------------------------------------------------------------

..  autoclass:: {{ item }}
    :members:

{% endfor %}
{% endif %}
{% endblock %}

{% block function_details %}
{% if functions %}
{% for item in functions %}
{{ item }}()
--------------------------------------------------------------

..  autofunction:: {{ item }}

{%- endfor %}
{% endif %}
{% endblock %}

{% block exception_details %}
{% if exceptions %}
{% for item in exceptions %}
{{ item }}()
--------------------------------------------------------------

..  autoexception:: {{ item }}

{%- endfor %}
{% endif %}
{% endblock %}