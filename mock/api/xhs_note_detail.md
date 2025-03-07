### xhs_note_detail

> 根据笔记链接获取【笔记详情】（xhs_note_detail） 功能描述： 根据提供的笔记URL和cookie，抓取该笔记的详细信息。 参数： noteUrl：笔记的URL地址。 cookieStr：小红书的cookie字符串，用于身份验证。

Request Param

```json
{
  "cookieStr": "abRequestId=9e9cb851-d530-5a26-b838-687d2a4faa0d; a1=18e30df561b6m2g7f2vlqeneli4de3umpeyqgpxyo50000180905; webId=827af36b4a294c71548a24dac603d34d; gid=yYdq8fiKKKU8yYdq8fi2KdUCyDK6JkWiJh1AvvldId134A28fdq76k888yY8j828YJyjSjjd; web_session=0400698f5a365056f008b01746354bf6fe9684; webBuild=4.57.0; xsecappid=xhs-pc-web; loadts=1740473338026; acw_tc=0ad520f117404733429918338e11a27d594ebea94ade61938cf5f0f7131988; websectiga=984412fef754c018e472127b8effd174be8a5d51061c991aadd200c69a2801d6; sec_poison_id=b63b9d6c-ac46-41af-9f33-5f1508c193fa; unread={%22ub%22:%2267b914b700000000280355c1%22%2C%22ue%22:%2267bc7a64000000002901f6f2%22%2C%22uc%22:28}",
  "noteUrl": "https://www.xiaohongshu.com/explore/66b425300000000005022f70?xsec_token=ABGif3t5zWZrkdspxKO796OXLDCEIQCJW7F3MsQrpro_g="
}
```

Response Param 
```json
{
  "code": 0,
  "data": {
    "note": {
      "note_last_update_time": "2024-08-08 09:53:52",
      "note_model_type": "note",
      "video_h266_url": null,
      "auther_avatar": "https://sns-avatar-qc.xhscdn.com/avatar/6724d476d0a6d335db29db64.jpg",
      "note_card_type": "normal",
      "note_desc": "#壁纸[话题]# #ootd每日穿搭[话题]# #高清壁纸[话题]# #手机壁纸[话题]#",
      "comment_count": "4",
      "note_liked_count": "7",
      "share_count": "0",
      "video_a1_url": null,
      "auther_home_page_url": "https://www.xiaohongshu.com/user/profile/64c1c2d70000000014036780",
      "auther_user_id": "64c1c2d70000000014036780",
      "collected_count": "2",
      "note_url": "https://www.xiaohongshu.com/explore/66b425300000000005022f70?xsec_token=ABGif3t5zWZrkdspxKO796OXLDCEIQCJW7F3MsQrpro_g=",
      "video_id": null,
      "note_create_time": "2024-08-08 09:53:52",
      "note_display_title": "随意做了几张可爱的壁纸，原图放评论区了",
      "note_image_list": [
        "http://sns-webpic-qc.xhscdn.com/202503071646/0f35ee8c4257e6ada94240b6e9c790c2/1040g2sg3167joubgio705p61obbl6ps0u6m0pvg!nd_dft_wlteh_webp_3",
        "http://sns-webpic-qc.xhscdn.com/202503071646/2ecedfe54215636e518522d2552228c1/1040g2sg3167joubgio7g5p61obbl6ps0jhkbtrg!nd_dft_wlteh_webp_3",
        "http://sns-webpic-qc.xhscdn.com/202503071646/047b29bf56af795458352628899b3e06/1040g2sg3167joubgio805p61obbl6ps0el694kg!nd_dft_wlteh_webp_3",
        "http://sns-webpic-qc.xhscdn.com/202503071646/8a1b8e822288263450032d5ffbaffce6/1040g2sg3167joubgio8g5p61obbl6ps0aao99h8!nd_dft_wlteh_webp_3"
      ],
      "note_tags": [
        "壁纸",
        "ootd每日穿搭",
        "高清壁纸",
        "手机壁纸"
      ],
      "video_h264_url": null,
      "video_h265_url": null,
      "auther_nick_name": "赫耳墨斯",
      "note_duration": null,
      "note_id": "66b425300000000005022f70",
      "note_liked": false,
      "collected": false
    }
  },
  "msg": "",
  "tips": "技术支持:https://alidocs.dingtalk.com/i/nodes/XPwkYGxZV3vqx0nMSq3ayZ66WAgozOKL"
}
```