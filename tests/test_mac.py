__author__ = 'markus'


import security

out = security.MessageAuthenticationCode("secret").get_mac_for_message("200 OK\nasdasd: 2323\n\nblah")
print out