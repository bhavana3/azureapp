<html>
<head>
</head>
<body>
<%var i=0;%>
{% if result != None %}
{%for jj in result %}
<% out.println(i++);%>
{% endfor %}
{% endif %}

</body>
</html>