# apns-testing-server
A Python server implementation of APNS v2, for use in client debugging. Note, currently does not support SSL or appropriate error code responses.

Usage:

  python apns_test_server # run the server

Testing:

  python apns_test_server & # run the server
  python test_client.py # send a valid sample request
