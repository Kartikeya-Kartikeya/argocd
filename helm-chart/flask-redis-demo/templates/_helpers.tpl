{{- define "flask-redis-demo.name" -}}
flask-redis-demo
{{- end }}

{{- define "flask-redis-demo.labels" -}}
app.kubernetes.io/name: {{ include "flask-redis-demo.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}