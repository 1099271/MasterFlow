### xhs_search_note

> 根据【关键词】搜索【小红书笔记】（xhs_search_note） 功能描述： 根据提供的关键词、cookie、排序方式（sort）、总笔记数（totalNumber）和笔记类型（noteType），搜索小红书上的笔记。 参数： cookieStr：小红书的cookie字符串，用于身份验证。 sort：排序方式，指定搜索结果的排序规则。 totalNumber：要抓取的笔记总数。 keywords：用于搜索的关键词。 noteType：笔记的类型，用于过滤搜索结果。

Request Params
```json
{
  "cookieStr": "abRequestId=9e9cb851-d530-5a26-b838-687d2a4faa0d; a1=18e30df561b6m2g7f2vlqeneli4de3umpeyqgpxyo50000180905; webId=827af36b4a294c71548a24dac603d34d; gid=yYdq8fiKKKU8yYdq8fi2KdUCyDK6JkWiJh1AvvldId134A28fdq76k888yY8j828YJyjSjjd; web_session=0400698f5a365056f008b01746354bf6fe9684; webBuild=4.57.0; xsecappid=xhs-pc-web; loadts=1740473338026; acw_tc=0ad520f117404733429918338e11a27d594ebea94ade61938cf5f0f7131988; websectiga=984412fef754c018e472127b8effd174be8a5d51061c991aadd200c69a2801d6; sec_poison_id=b63b9d6c-ac46-41af-9f33-5f1508c193fa; unread={%22ub%22:%2267b914b700000000280355c1%22%2C%22ue%22:%2267bc7a64000000002901f6f2%22%2C%22uc%22:28}",
  "keywords": "摩梭族",
  "noteType": 2,
  "sort": 0,
  "totalNumber": 10
}
```

Response Param
```json
{
  "data": [
    {
      "note_cover_url_pre": "http://sns-webpic-qc.xhscdn.com/202503071654/00858c9a3bff017a485c1bc2aaa4f79a/1040g2sg30ub2jb0jle005pb5purv3kd2tvt7hhg!nc_n_webp_prv_1",
      "note_xsec_token": "ABwI6y98bvx7dSMQKtWGyhC7AERxYP6ZUkH5O6ywihVtQ=",
      "auther_home_page_url": "https://www.xiaohongshu.com/user/profile/6565cfb7000000003c01d1a2",
      "note_cover_url_default": "http://sns-webpic-qc.xhscdn.com/202503071654/9070cad404e09541f9410e7951b166c2/1040g2sg30ub2jb0jle005pb5purv3kd2tvt7hhg!nc_n_webp_mw_1",
      "note_cover_width": "1668",
      "note_id": "65b18c34000000000c0050f6",
      "note_url": "https://www.xiaohongshu.com/explore/65b18c34000000000c0050f6?xsec_token=ABwI6y98bvx7dSMQKtWGyhC7AERxYP6ZUkH5O6ywihVtQ=",
      "auther_avatar": "https://sns-avatar-qc.xhscdn.com/avatar/65aa73ea5e0a901295d5d39b.jpg?imageView2/2/w/80/format/jpg",
      "auther_nick_name": "野鲨",
      "note_cover_height": "2388",
      "note_liked_count": "5345",
      "auther_user_id": "6565cfb7000000003c01d1a2",
      "note_card_type": "normal",
      "note_display_title": "中国最后的母系氏族 没有婚姻制度非常幸福",
      "note_model_type": "note",
      "note_liked": false
    },
    {
      "note_cover_url_pre": "http://sns-webpic-qc.xhscdn.com/202503071654/aef3442bc98a73453b779b7fdd835255/1000g00828sht8eifo0005o1e95bgbv22phsbvug!nc_n_webp_prv_1",
      "note_xsec_token": "ABn5O1g0mc7dBkFQOeKnqS8YCC5BIp27ayPAA9CySZsko=",
      "auther_home_page_url": "https://www.xiaohongshu.com/user/profile/602e4957000000000101fc42",
      "note_cover_url_default": "http://sns-webpic-qc.xhscdn.com/202503071654/318d364ed0e8ce435b5080ba33526f6d/1000g00828sht8eifo0005o1e95bgbv22phsbvug!nc_n_webp_mw_1",
      "note_cover_width": "1440",
      "note_id": "64244bab000000002702b7f4",
      "note_url": "https://www.xiaohongshu.com/explore/64244bab000000002702b7f4?xsec_token=ABn5O1g0mc7dBkFQOeKnqS8YCC5BIp27ayPAA9CySZsko=",
      "auther_avatar": "https://sns-avatar-qc.xhscdn.com/avatar/62b41068732d149a6a1b8807.jpg?imageView2/2/w/80/format/jpg",
      "auther_nick_name": "Nnnmko",
      "note_cover_height": "1920",
      "note_liked_count": "16646",
      "auther_user_id": "602e4957000000000101fc42",
      "note_card_type": "normal",
      "note_display_title": "纪录片｜中国唯一现存的母系社会「摩梭族」",
      "note_model_type": "note",
      "note_liked": false
    }
  ],
  "msg": "",
  "tips": "技术支持:https://alidocs.dingtalk.com/i/nodes/XPwkYGxZV3vqx0nMSq3ayZ66WAgozOKL",
  "code": 0
}
```