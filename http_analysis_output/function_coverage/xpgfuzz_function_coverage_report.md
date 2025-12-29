# xpgfuzz 函数级覆盖分析报告

生成时间: 2025-12-28 20:26:25

## 概述

- 分析的文件数: 91
- 分析的函数数: 778
- 覆盖不足的函数数: 776

## 覆盖不足的函数

| 文件 | 函数名 | 起始行 | 行覆盖率 | 已执行/总行数 |
|------|--------|--------|----------|---------------|
| lighttpd1-gcov/src/http_kv.c | http_version_buf | 1 | 0.0% | 0/51 |
| lighttpd1-gcov/src/http-header-glue.c | http_response_delay | 1 | 0.0% | 0/51 |
| lighttpd1-gcov/src/http-header-glue.c | http_response_check_1xx | 1091 | 0.0% | 0/51 |
| lighttpd1-gcov/src/gw_backend.c | gw_hash | 1 | 0.0% | 0/51 |
| lighttpd1-gcov/src/ck.h | __attribute_nonnull__ | 59 | 0.0% | 0/51 |
| lighttpd1-gcov/src/ck.h | __attribute_nonnull__ | 65 | 0.0% | 0/51 |
| lighttpd1-gcov/src/ck.h | __attribute_nonnull__ | 85 | 0.0% | 0/34 |
| lighttpd1-gcov/src/ck.h | __attribute_nonnull__ | 93 | 0.0% | 0/26 |
| lighttpd1-gcov/src/ck.h | __attribute_nonnull__ | 99 | 0.0% | 0/20 |
| lighttpd1-gcov/src/mod_auth.c | http_auth_cache_entry_init | 1 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | http_auth_cache_entry_free | 60 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | http_auth_cache_free | 88 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | http_auth_cache_init | 96 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | http_auth_cache_hash | 107 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | http_auth_cache_query | 122 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_tag_old_entries | 132 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_periodic_cleanup | 154 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | TRIGGER_FUNC | 170 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_send_400_bad_request | 191 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_send_401_unauthorized_basic | 739 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_basic_misconfigured | 751 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_check_basic | 767 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_digest_mutate | 784 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_append_nonce | 902 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_digest_www_authenticate | 993 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_send_401_unauthorized_digest | 1057 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_digest_authentication_info | 1112 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_digest_get | 1125 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_digest_misconfigured | 1135 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_digest_parse_authorization | 1210 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_digest_validate_userstar | 1227 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_digest_validate_params | 1297 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_digest_validate_nonce | 1362 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_check_digest | 1446 | 0.0% | 0/51 |
| lighttpd1-gcov/src/connections.c | connection_set_fdevent_interest | 744 | 0.0% | 0/51 |
| lighttpd1-gcov/src/network.c | network_abstract_socket_dec | 139 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_extforward.c | CONNECTION_FUNC | 1 | 0.0% | 0/51 |
| lighttpd1-gcov/src/mod_extforward.c | CONNECTION_FUNC | 1148 | 0.0% | 0/51 |
| lighttpd1-gcov/src/ls-hpack/lshpack.c | lshpack_arr_push | 1 | 0.0% | 0/51 |
| lighttpd1-gcov/src/ls-hpack/lshpack.c | henc_hist_size | 209 | 0.0% | 0/51 |
| lighttpd1-gcov/src/ls-hpack/lshpack.c | lshpack_enc_init | 286 | 0.0% | 0/51 |
| lighttpd1-gcov/src/ls-hpack/lshpack.c | lshpack_enc_cleanup | 293 | 0.0% | 0/51 |
| lighttpd1-gcov/src/ls-hpack/lshpack.c | henc_use_hist | 327 | 0.0% | 0/51 |
| lighttpd1-gcov/src/ls-hpack/lshpack.c | lshpack_enc_use_hist | 341 | 0.0% | 0/51 |
| lighttpd1-gcov/src/ls-hpack/lshpack.c | lshpack_enc_hist_used | 363 | 0.0% | 0/51 |
| lighttpd1-gcov/src/ls-hpack/lshpack.c | lshpack_enc_get_static_nameval | 381 | 0.0% | 0/51 |
| lighttpd1-gcov/src/ls-hpack/lshpack.c | lshpack_enc_get_static_name | 430 | 0.0% | 0/51 |
| lighttpd1-gcov/src/ls-hpack/lshpack.c | update_hash | 456 | 0.0% | 0/51 |
| lighttpd1-gcov/src/ls-hpack/lshpack.c | lshpack_enc_get_stx_tab_id | 478 | 0.0% | 0/51 |
| lighttpd1-gcov/src/ls-hpack/lshpack.c | henc_calc_table_id | 499 | 0.0% | 0/51 |

## 种子生成建议

### focus_files

建议重点关注以下文件的测试

| 文件 | 平均覆盖率 |
|------|-----------|
| lighttpd1-gcov/src/gw_backend.c | 0.0% |
| lighttpd1-gcov/src/mod_auth.c | 0.0% |
| lighttpd1-gcov/src/mod_extforward.c | 0.0% |
| lighttpd1-gcov/src/ls-hpack/lshpack.c | 0.0% |
| lighttpd1-gcov/src/mod_expire.c | 0.0% |

### focus_functions

建议生成针对以下函数的测试种子

| 文件 | 函数名 | 行覆盖率 |
|------|--------|----------|
| lighttpd1-gcov/src/http_kv.c | http_version_buf | 0.0% |
| lighttpd1-gcov/src/http-header-glue.c | http_response_delay | 0.0% |
| lighttpd1-gcov/src/http-header-glue.c | http_response_check_1xx | 0.0% |
| lighttpd1-gcov/src/gw_backend.c | gw_hash | 0.0% |
| lighttpd1-gcov/src/ck.h | __attribute_nonnull__ | 0.0% |
| lighttpd1-gcov/src/ck.h | __attribute_nonnull__ | 0.0% |
| lighttpd1-gcov/src/ck.h | __attribute_nonnull__ | 0.0% |
| lighttpd1-gcov/src/ck.h | __attribute_nonnull__ | 0.0% |
| lighttpd1-gcov/src/ck.h | __attribute_nonnull__ | 0.0% |
| lighttpd1-gcov/src/mod_auth.c | http_auth_cache_entry_init | 0.0% |

### uncovered_functions

发现 607 个完全未覆盖的函数，需要优先测试

| 文件 | 函数名 | 行覆盖率 |
|------|--------|----------|
| lighttpd1-gcov/src/http_kv.c | http_version_buf | 0.0% |
| lighttpd1-gcov/src/http-header-glue.c | http_response_delay | 0.0% |
| lighttpd1-gcov/src/http-header-glue.c | http_response_check_1xx | 0.0% |
| lighttpd1-gcov/src/gw_backend.c | gw_hash | 0.0% |
| lighttpd1-gcov/src/ck.h | __attribute_nonnull__ | 0.0% |
| lighttpd1-gcov/src/ck.h | __attribute_nonnull__ | 0.0% |
| lighttpd1-gcov/src/ck.h | __attribute_nonnull__ | 0.0% |
| lighttpd1-gcov/src/ck.h | __attribute_nonnull__ | 0.0% |
| lighttpd1-gcov/src/ck.h | __attribute_nonnull__ | 0.0% |
| lighttpd1-gcov/src/mod_auth.c | http_auth_cache_entry_init | 0.0% |
| lighttpd1-gcov/src/mod_auth.c | http_auth_cache_entry_free | 0.0% |
| lighttpd1-gcov/src/mod_auth.c | http_auth_cache_free | 0.0% |
| lighttpd1-gcov/src/mod_auth.c | http_auth_cache_init | 0.0% |
| lighttpd1-gcov/src/mod_auth.c | http_auth_cache_hash | 0.0% |
| lighttpd1-gcov/src/mod_auth.c | http_auth_cache_query | 0.0% |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_tag_old_entries | 0.0% |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_periodic_cleanup | 0.0% |
| lighttpd1-gcov/src/mod_auth.c | TRIGGER_FUNC | 0.0% |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_send_400_bad_request | 0.0% |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_send_401_unauthorized_basic | 0.0% |

