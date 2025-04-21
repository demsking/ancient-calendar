FROM python:3.11-alpine

ENV PATH="/opt/ancient-calendar/bin:/usr/local/bin:$PATH"
ENV PYTHONPATH="/opt/ancient-calendar:/usr/local/lib/python3.11/site-packages"
ENV PYTHONUNBUFFERED="1"
ENV PYTHONDONTWRITEBYTECODE="1"

ENV HOST="0.0.0.0"
ENV PORT=4241

ENV TIMEZONE="UTC"

ENV LOG_LEVEL="info"
ENV LOG_FILE=

# Set the shell to /bin/ash and enable pipefail
SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

# Upgrade pip and setuptools to the latest version
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Build Python dependencies
COPY build/requirements.txt /opt/ancient-calendar/
RUN pip install --no-cache-dir -r /opt/ancient-calendar/requirements.txt

# Binaries
COPY bin/* /opt/ancient-calendar/bin/
RUN chmod +x /opt/ancient-calendar/bin/* \
  && mkdir -p /var/cache/ancient-calendar

# Copy application files
COPY pyproject.toml LICENSE DOCUMENTATION.md /opt/ancient-calendar/
COPY server/ /opt/ancient-calendar/server

VOLUME "/var/cache/ancient-calendar"
VOLUME "/root/.cache/huggingface"

EXPOSE 4241

CMD ["ancient-calendar"]
