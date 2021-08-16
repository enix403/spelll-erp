# type: ignore

from typing import TYPE_CHECKING

from passlib.hash import (
    argon2,
    bcrypt,
    bcrypt_sha256,
    cisco_asa,
    cisco_pix,
    cisco_type7,
    bigcrypt,
    bsdi_crypt,
    crypt16,
    des_crypt,
    hex_md4,
    hex_md5,
    hex_sha1,
    hex_sha256,
    hex_sha512,
    htdigest,
    django_bcrypt,
    django_bcrypt_sha256,
    django_des_crypt,
    django_disabled,
    django_pbkdf2_sha1,
    django_pbkdf2_sha256,
    django_salted_md5,
    django_salted_sha1,
    fshp,
    apr_md5_crypt,
    md5_crypt,
    plaintext,
    unix_disabled,
    unix_fallback,
    mssql2000,
    mssql2005,
    mysql323,
    mysql41,
    oracle10,
    oracle11,
    atlassian_pbkdf2_sha1,
    cta_pbkdf2_sha1,
    dlitz_pbkdf2_sha1,
    grub_pbkdf2_sha512,
    ldap_pbkdf2_sha1,
    ldap_pbkdf2_sha256,
    ldap_pbkdf2_sha512,
    pbkdf2_sha1,
    pbkdf2_sha256,
    pbkdf2_sha512,
    phpass,
    postgres_md5,
    ldap_hex_md5,
    ldap_hex_sha1,
    roundup_plaintext,
    scram,
    scrypt,
    sha1_crypt,
    sha256_crypt,
    sha512_crypt,
    sun_md5_crypt,
    bsd_nthash,
    lmhash,
    msdcc,
    msdcc2,
    nthash
)

if TYPE_CHECKING:
    from passlib.handlers.argon2 import argon2
    from passlib.handlers.bcrypt import bcrypt, bcrypt_sha256
    from passlib.handlers.cisco import cisco_asa, cisco_pix, cisco_type7
    from passlib.handlers.des_crypt import bigcrypt, bsdi_crypt, crypt16, des_crypt
    from passlib.handlers.digests import hex_md4, hex_md5, hex_sha1, hex_sha256, hex_sha512, htdigest
    from passlib.handlers.django import django_bcrypt, django_bcrypt_sha256, django_des_crypt, django_disabled, django_pbkdf2_sha1, django_pbkdf2_sha256, django_salted_md5, django_salted_sha1
    from passlib.handlers.fshp import fshp
    from passlib.handlers.ldap_digests import ldap_bcrypt, ldap_bsdi_crypt, ldap_des_crypt, ldap_md5, ldap_md5_crypt, ldap_plaintext, ldap_salted_md5, ldap_salted_sha1, ldap_salted_sha256, ldap_salted_sha512, ldap_sha1, ldap_sha1_crypt, ldap_sha256_crypt, ldap_sha512_crypt
    from passlib.handlers.md5_crypt import apr_md5_crypt, md5_crypt
    from passlib.handlers.misc import plaintext, unix_disabled, unix_fallback
    from passlib.handlers.mssql import mssql2000, mssql2005
    from passlib.handlers.mysql import mysql323, mysql41
    from passlib.handlers.oracle import oracle10, oracle11
    from passlib.handlers.pbkdf2 import atlassian_pbkdf2_sha1, cta_pbkdf2_sha1, dlitz_pbkdf2_sha1, grub_pbkdf2_sha512, ldap_pbkdf2_sha1, ldap_pbkdf2_sha256, ldap_pbkdf2_sha512, pbkdf2_sha1, pbkdf2_sha256, pbkdf2_sha512
    from passlib.handlers.phpass import phpass
    from passlib.handlers.postgres import postgres_md5
    from passlib.handlers.roundup import ldap_hex_md5, ldap_hex_sha1, roundup_plaintext
    from passlib.handlers.scram import scram
    from passlib.handlers.scrypt import scrypt
    from passlib.handlers.sha1_crypt import sha1_crypt
    from passlib.handlers.sha2_crypt import sha256_crypt, sha512_crypt
    from passlib.handlers.sun_md5_crypt import sun_md5_crypt
    from passlib.handlers.windows import bsd_nthash, lmhash, msdcc, msdcc2, nthash