import threading
import urllib.parse
from socket import *

import google_query
import keywords_finder
from RequestHTTP import RequestHTTP


class PythonServer(object):
    """
    Python custom server

    Parameters
    -----------
    server_port = port for the server

    Attributes
    -----------
    server_port = the server port
    """
    def __init__(self, server_port=80):
        self.server_port = server_port
        self.__header = "HTTP/1.1 200 OK\nContent-Type: text/html; encoding=utf8\n\n"
        self.__querySize = 3
        self.__keywords_size = 5

    def start(self):
        """Run the server and manage the http request"""
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind(('', self.server_port))
        server_socket.listen(1)
        while True:
            print('\nReady to serve... Port: ' + str(self.server_port))
            connection_socket, addr = server_socket.accept()
            request = connection_socket.recv(2048)
            print(request)
            threading.Thread(target=self.response_thread, args=(connection_socket, request)).start()
        server_socket.close()

    def response_thread(self, connection_socket, request):
        request_http = RequestHTTP(request)
        print("\nRequest type = " + request_http.request_type)
        print("Filename = " + request_http.filename)
        if request_http.filename != "perform_search.html":
            try:
                f = open(request_http.filename)
                output_data = f.read()
                connection_socket.send(str.encode(self.__header))
                connection_socket.send(str.encode(output_data))
                f.close()
            except IOError:
                print("404 Not Found")
                connection_socket.send(str.encode('\nHTTP/1.1 404 Not Found\n\n'))
            except IndexError:
                print("400 Bad Request")
                connection_socket.send(str.encode('\nHTTP/1.1 400 Bad Request\n\n'))
        else:
            self.handle_perform_search_request(connection_socket, request_http)
        connection_socket.close()

    def array_to_images(self, images):
        """Convert a links array to a string of html images"""
        out = ""
        for i in range(len(images)):
            out += "<div class='col s4'><img class='materialboxed responsive-img' src='" + images[i] +"'></div>"
        return out

    def array_to_videos(self, videos):
        """Convert a links array to a string of html videos"""
        out = ""
        for i in range(len(videos)):
            out += "<div class='col s4'><div class='video-container'><iframe width='640' height='360' src='" + videos[i] + "' frameborder='0' allowfullscreen></iframe></div></div>"
        return out

    def array_to_articles(self, article):
        """Convert an array (title , link) to a string of html articles"""
        out = ""
        for title, link in article:
            try:
                img_link = google_query.get_image_url(title, 1)[0]
            except IndexError:
                img_link = ""
            out += "<div class='col s4'><div class='card'><div class='card-image'><img class='materialboxed' src='" + img_link + "'><span class='card-title'></span></div><div class='card-action'><a href='" + link + "'>" + title + "</a></div></div></div>"
        return out

    def create_keywords_table(self, request_http):
        """Convert the keywords string to a string of html table row"""
        keywords = request_http.keywords.split("+")
        out = ""
        for kw in keywords:
            kw = urllib.parse.unquote(kw)
            out += "<a href='perform_search.html?keywords=" + kw + "' class='collection-item'>" + kw + "</a>"
        return out

    def handle_perform_search_request(self, connection_socket, request_http):
        """Create a custom .hmtl page that show videos, images and articles for the keywords

        Parameters
        -----------
        connection_socket: connection socket
        request_http: the http request, with the attr self.keywords deifined
        """
        connection_socket.send(str.encode(self.__header))
        if hasattr(request_http, "keywords"):
            if request_http.keywords[:4] == "http":
                words_list = keywords_finder.get_word_more_frequent_from_url(request_http.keywords, limit=self.__keywords_size)
                request_http.keywords = '+'.join(words_list)
            else:
                words_list = keywords_finder.get_word_more_frequent_from_text(request_http.keywords, limit=self.__keywords_size)
                request_http.keywords = '+'.join(words_list)
            f = open("perform_search1.html")
            output_data = f.read()
            connection_socket.send(str.encode(output_data))
            f.close()
            # Insert Videos
            connection_socket.send(str.encode(self.array_to_videos(google_query.get_video_url(request_http.keywords, self.__querySize))))
            #
            f = open("perform_search2.html")
            output_data = f.read()
            connection_socket.send(str.encode(output_data))
            f.close()
            # Insert Images
            connection_socket.send(str.encode(self.array_to_images(google_query.get_image_url(request_http.keywords, self.__querySize))))
            #
            f = open("perform_search3.html")
            output_data = f.read()
            connection_socket.send(str.encode(output_data))
            f.close()
            # Insert Articles
            connection_socket.send(str.encode(self.array_to_articles(google_query.get_article(request_http.keywords, self.__querySize))))
            #
            f = open("perform_search4.html")
            output_data = f.read()
            connection_socket.send(str.encode(output_data))
            f.close()
            # Insert Keywords
            connection_socket.send(str.encode(self.create_keywords_table(request_http)))
            #
            f = open("perform_search5.html")
            output_data = f.read()
            connection_socket.send(str.encode(output_data))
            f.close()
            print("-> perform_search.html generated")


# Run the server
python_server = PythonServer(server_port=8080)
python_server.start()
