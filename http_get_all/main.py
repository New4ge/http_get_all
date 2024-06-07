import os
import re
import sys
import requests
import argparse
import urllib.parse

from requests import Response


def parse_command_line_arguments() -> argparse.Namespace:
    """
    Parse command line arguments and return the parsed arguments.

    :return: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Downloads files from url and create's respective directories."
    )
    parser.add_argument("-u", "--url", help="URL to parse")
    parser.add_argument('-d', '--directory', help="Directory to save files in.")
    return parser.parse_args()


def save_file(response: Response, directory: str) -> None:
    """
    Save the content of a response to a file.

    :param response: The response object containing the content to save.
    :param directory: The directory where the file will be saved.
    :return: None
    """
    filename = os.path.join(directory, urllib.parse.unquote(os.path.basename(response.url)))
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=131072):
            if chunk:
                file.write(chunk)


def parse_directory(response, directory):
    """
    :param response: The HTTP response object from a GET request.
    :param directory: The directory path where files should be saved.
    :return: None

    This method takes an HTTP response object and a directory path as parameters.
    It extracts the directory name from the response URL and creates a new directory
    with that name inside the given directory path. If the directory doesn't exist,
    it will be created.

    If the response content type is 'text/html', it extracts all the links from the
    HTML content and processes each link. If the link points to a directory (ends with
    '/'), it recursively calls the parse_directory method with the new directory path
    and the link's HTTP response. Otherwise, it calls the save_file method to save the
    file in the new directory.
    """
    # extract the directory name from the URL
    directory_name = urllib.parse.unquote(os.path.basename(response.url.rstrip('/')))

    new_directory = os.path.join(directory, directory_name)
    # create the directory if it doesn't exist
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)

    # check if the response is HTML
    if 'text/html' in response.headers.get('Content-Type', ''):
        # extract all the links from the HTML
        links = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)
        for link in links:
            # join the link with the base URL
            absolute_link = f"{response.url}/{link}"
            # make a GET request to the link
            link_response = requests.get(absolute_link, stream=True)
            # check if it was a directory or a file
            if link_response.url.endswith('/'):
                parse_directory(link_response, new_directory)
            else:
                save_file(link_response, new_directory)


if __name__ == "__main__":
    args = parse_command_line_arguments()

    # check if directory path is valid
    if not os.path.exists(args.directory):
        print("Directory doesn't exist.")
        sys.exit(1)

    res = requests.get(args.url, stream=True)
    if res.status_code != 200:
        print("Invalid URL.")

    # check if it was a directory or a file.
    if res.url.endswith('/'):
        parse_directory(res, args.directory)
    else:
        save_file(res, args.directory)
