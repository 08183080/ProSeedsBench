# 种子生成洞察报告

生成时间: 2025-12-28 20:33:32

## 覆盖分析总结

- 完全未覆盖的函数: 607
- 部分覆盖的函数: 169
- 低覆盖率文件: 52

## 优先级函数（前20个）

| 文件 | 函数名 | 起始行 | 总行数 | 优先级 |
|------|--------|--------|--------|--------|
| lighttpd1-gcov/src/http_kv.c | http_version_buf | 1 | N/A | high |
| lighttpd1-gcov/src/http-header-glue.c | http_response_delay | 1 | N/A | high |
| lighttpd1-gcov/src/http-header-glue.c | http_response_check_1xx | 1091 | N/A | high |
| lighttpd1-gcov/src/gw_backend.c | gw_hash | 1 | N/A | high |
| lighttpd1-gcov/src/ck.h | __attribute_nonnull__ | 59 | N/A | high |
| lighttpd1-gcov/src/ck.h | __attribute_nonnull__ | 65 | N/A | high |
| lighttpd1-gcov/src/mod_auth.c | http_auth_cache_entry_init | 1 | N/A | high |
| lighttpd1-gcov/src/mod_auth.c | http_auth_cache_entry_free | 60 | N/A | high |
| lighttpd1-gcov/src/mod_auth.c | http_auth_cache_free | 88 | N/A | high |
| lighttpd1-gcov/src/mod_auth.c | http_auth_cache_init | 96 | N/A | high |
| lighttpd1-gcov/src/mod_auth.c | http_auth_cache_hash | 107 | N/A | high |
| lighttpd1-gcov/src/mod_auth.c | http_auth_cache_query | 122 | N/A | high |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_tag_old_entries | 132 | N/A | high |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_periodic_cleanup | 154 | N/A | high |
| lighttpd1-gcov/src/mod_auth.c | TRIGGER_FUNC | 170 | N/A | high |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_send_400_bad_request | 191 | N/A | high |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_send_401_unauthorized_basic | 739 | N/A | high |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_basic_misconfigured | 751 | N/A | high |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_check_basic | 767 | N/A | high |
| lighttpd1-gcov/src/mod_auth.c | mod_auth_digest_mutate | 784 | N/A | high |

## 目标文件（前10个）

| 文件 | 平均覆盖率 | 未覆盖函数数 | 优先级 |
|------|-----------|-------------|--------|
| lighttpd1-gcov/src/gw_backend.c | 0.0% | 1 | high |
| lighttpd1-gcov/src/mod_auth.c | 0.0% | 25 | high |
| lighttpd1-gcov/src/mod_extforward.c | 0.0% | 2 | high |
| lighttpd1-gcov/src/ls-hpack/lshpack.c | 0.0% | 42 | high |
| lighttpd1-gcov/src/mod_expire.c | 0.0% | 1 | high |
| lighttpd1-gcov/src/ls-hpack/lsxpack_header.h | 0.0% | 9 | high |
| lighttpd1-gcov/src/http_header.c | 0.0% | 1 | high |
| lighttpd1-gcov/src/rand.c | 0.0% | 1 | high |
| lighttpd1-gcov/src/h2.c | 0.0% | 65 | high |
| lighttpd1-gcov/src/algo_xxhash.h | 0.0% | 83 | high |

## 种子生成模板建议

### http_methods

生成不同HTTP方法的请求来覆盖HTTP处理函数

目标函数: http_version_buf, http_response_delay, http_response_check_1xx, gw_hash, __attribute_nonnull__

模板示例: `HTTP/1.1 {method} /path HTTP/1.1
Host: example.com

`

### http_headers

生成包含各种HTTP头的请求来覆盖头部处理函数

目标函数: http_version_buf, http_response_delay, http_response_check_1xx, gw_hash, __attribute_nonnull__

模板示例: `GET /path HTTP/1.1
Host: example.com
{header_name}: {header_value}

`

### authentication

生成包含认证信息的请求来覆盖认证相关函数

目标函数: http_auth_cache_entry_init, http_auth_cache_entry_free, http_auth_cache_free, http_auth_cache_init, http_auth_cache_hash

模板示例: `GET /path HTTP/1.1
Host: example.com
Authorization: {auth_type} {credentials}

`

