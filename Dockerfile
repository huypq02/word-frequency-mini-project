FROM python:3.13
WORKDIR /usr/local/app

# # Download NLTK data as root before switching to non-root user
# RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY src ./src
EXPOSE 5000

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

# Set cache directories to /tmp to avoid permission issues
ENV MPLCONFIGDIR=/tmp/matplotlib
ENV NLTK_DATA=/tmp/nltk_data

CMD [ "python", "-m", "src.app.main"]
