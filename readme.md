# 微信Image中的dat文件转png
## 突发奇想
定期清微信垃圾的时候发现image文件夹内的文件都是dat文件，然后就想把dat转png。

## 步骤
- 获取加密密码

    用十六进制打开dat文件，获取前两个字节，然后跟FFD8进行异或，得到加密密码
- 转换格式
    
    读取dat文件，执行异或操作，最后写入png文件。


## Future Work
优化程序

## 参考
[python 读取文件、并以十六进制的方式写入到新文件](https://www.jianshu.com/p/69d3d862e7fd)
[解密微信电脑版image文件夹下缓存的用户图片](https://blog.csdn.net/huichendelvxing/article/details/117118022?utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~aggregatepage~first_rank_ecpm_v1~rank_v31_ecpm-1-117118022.pc_agg_new_rank&utm_term=%E5%BE%AE%E4%BF%A1Image%E6%96%87%E4%BB%B6%E5%A4%B9%E9%87%8C%E7%9A%84thumb%E6%96%87%E4%BB%B6%E6%98%AF%E4%BB%80%E4%B9%88&spm=1000.2123.3001.4430)
[Python-PyQt5-图形可视化界面(5)--打开文件或文件夹--QFileDialog](https://www.jianshu.com/p/98e8218b2309)
[利用正则表达式从文件路径中提取出文件名(包含后缀)](https://blog.csdn.net/kpchen_0508/article/details/40921457)