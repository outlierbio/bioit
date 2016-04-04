FROM outlierbio/bioit

# Set up GeneTorrent
RUN cd /opt && \
  wget https://cghub.ucsc.edu/software/downloads/GeneTorrent/3.8.7/GeneTorrent-download-3.8.7-207-CentOS6.4.x86_64.tar.gz && \
  tar -xvf GeneTorrent-download-3.8.7-207-CentOS6.4.x86_64.tar.gz && \
  rm GeneTorrent-download-3.8.7-207-CentOS6.4.x86_64.tar.gz
ENV PATH $PATH:/opt/cghub/bin

