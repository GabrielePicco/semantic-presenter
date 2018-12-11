class RequestHTTP(object):
    """
    Http Request

    Parameters
    -----------
    request : The string request

    Attributes
    -----------
    request_type : the request type GET / POST
    filename : requested filename
    """

    def __init__(self, request):
        request = request.decode()
        flname = request.split()[1]
        self.request_type = request.split()[0]
        self.filename = self.get_file_name(flname)
        if self.request_type == "POST":
            self.set_post_attribute(request)

    def get_file_name(self, str_data):
        """parse string to extract filename and parameters

        Parameters
        -----------
        str_data: a string that contain the filename and maybe the parameters

        Returns
        --------
        filename: the name of the file requested

        set the request parameters as attributes of the self object

        """
        if "?" in str(str_data):
            scompact = str_data.split("?")
            str_data = scompact[0]
            get_param = scompact[1].split("&")
            for i in range(len(get_param)):
                self.set_request_attribute(get_param[i])
        if str_data == "/":
            str_data = "/index.html"
        return str_data[1:]

    def set_post_attribute(self, request):
        """set the request if the request_type is a POST
        Parameters
        -----------
        request: the request string that contain the parameters (param=value)
        """
        index = request.find("\r\n\r\n")
        if index != -1:
            get_param = request[index+4:].split("&")
            for i in range(len(get_param)):
                self.set_request_attribute(get_param[i])

    def set_request_attribute(self, param_str):
        """set the request parameters as attributes of the self object
        Parameters
        -----------
        param_str: a string that contain the parameters (param=value)
        """
        try:
            param = param_str.split("=")
            setattr(self, param[0], param[1])
        except IndexError:
            print("Bad Request")
