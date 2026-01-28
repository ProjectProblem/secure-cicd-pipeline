# Use Alpine-based Python for better security
FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Install build dependencies for Python packages
RUN apk add --no-cache gcc musl-dev linux-headers

# Create non-root user for security
RUN adduser -D -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:5000/ || exit 1

# Run application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "app:app"]
