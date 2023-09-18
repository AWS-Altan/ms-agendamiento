FROM centos:7.6.1810
RUN yum -y install epel-release
RUN yum -y update 
RUN yum -y install net-tools httpd perl perl-CGI* perl-SOAP* perl-DBD* perl-JSON* perl-Time* perl-XML* pip phyton php make gcc gcc-c++ mysql
EXPOSE 80
#RUN mkdir -p /var/www/cgi-bin/noti
RUN mkdir -p /var/www/cgi-bin/auditor
RUN mkdir -p /var/www/cgi-bin/log/notificador
COPY auditor/* /var/www/cgi-bin/auditor/
#COPY noti/* /var/www/cgi-bin/noti/
RUN chown -R apache:apache /var/www/cgi-bin/log
#RUN chown -R apache:apache /var/www/cgi-bin/noti
RUN chown -R apache:apache /var/www/cgi-bin/auditor
RUN rm -f /etc/localtime
RUN ln -s /usr/share/zoneinfo/America/Mexico_City /etc/localtime
RUN ln -s /var/www/cgi-bin/log/bacth /var/www/cgi-bin/bacth
COPY index.html /var/www/html/index.html
COPY httpd.conf /etc/httpd/conf/httpd.conf
RUN chmod 755 /var/www/cgi-bin/auditor/*.cgi
CMD ["/usr/sbin/httpd","-D","FOREGROUND"]
