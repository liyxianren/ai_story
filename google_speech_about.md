Speech-to-Text 支持的语言

bookmark_border
版本说明
本页面列出了 Cloud Speech-to-Text 支持的所有语言。 语言是在识别请求的 languageCode 参数中指定的。如需详细了解如何发送识别请求并指定转录语言，请参阅如何执行语音识别的方法指南。如需详细了解每种语言的类令牌，请参阅类令牌页面。

下表列出了适用于每种语言的模型。Cloud Speech-to-Text 提供多个识别模型，每个模型都针对不同的音频类型进行了微调。default 和 command_and_search 识别模型支持所有可用语言。command_and_search 模型针对短音频剪辑（例如语音指令或语音搜索）进行了优化。default 模型可用于转录任何音频类型。

一些语言支持其他模型，并针对其他音频类型进行了优化：enhanced phone_call 和 enhanced video。与 default 模型相比，这些模型可以更准确地识别从这些音频来源捕获的语音。如需了解详情，请参阅增强型模型页面。如果这些其他模型中的任何模型适用于您的语言，则会与您的语言的 default 和 command_and_search 模型一并列出。如果您的语言中只列出 default 和 command_and_search 模型，则目前没有其他模型可用。

仅使用下表中显示的语言代码。以下语言代码由 Google 正式维护和在外部监控。使用其他语言代码可能会导致重大更改。

按支持的功能过滤：

 全部
 脏话过滤器
 语音标点符号 （添加语音标点符号）
 语音表情符号 （添加语音表情符号）
 字词级置信度（预览版） （字词级置信度）
 自动加注标点符号 （自动添加标点符号）
 讲话人区分（预览版） （自动检测不同的讲话人）
 模型自适应（预览版） （自定义字词识别）
按语言过滤：
语言...
名称	BCP-47	模型	单独一条话语	自动加注标点符号	区分	模型自适应	字词级置信度	脏话过滤器	口头标点符号	口头表情符号
南非荷兰语（南非）	af-ZA	command_and_search	False			✔		✔		
南非荷兰语（南非）	af-ZA	command_and_search	True			✔		✔		
南非荷兰语（南非）	af-ZA	default	False			✔		✔		
阿尔巴尼亚语（阿尔巴尼亚）	sq-AL	command_and_search	False					✔		
阿尔巴尼亚语（阿尔巴尼亚）	sq-AL	command_and_search	True					✔		
阿尔巴尼亚语（阿尔巴尼亚）	sq-AL	default	False					✔		
阿姆哈拉语（埃塞俄比亚）	am-ET	command_and_search	False					✔		
阿姆哈拉语（埃塞俄比亚）	am-ET	command_and_search	True					✔		
阿姆哈拉语（埃塞俄比亚）	am-ET	default	False					✔		
阿拉伯语（阿尔及利亚）	ar-DZ	command_and_search	False					✔		
阿拉伯语（阿尔及利亚）	ar-DZ	command_and_search	True					✔		
阿拉伯语（阿尔及利亚）	ar-DZ	default	False					✔		
阿拉伯语（阿尔及利亚）	ar-DZ	latest_long	False	✔			✔	✔		
阿拉伯语（阿尔及利亚）	ar-DZ	latest_long	True	✔		✔	✔	✔		
阿拉伯语（阿尔及利亚）	ar-DZ	latest_short	False	✔		✔	✔	✔		
阿拉伯语（阿尔及利亚）	ar-DZ	latest_short	True	✔		✔	✔	✔		
阿拉伯语（巴林）	ar-BH	command_and_search	False			✔		✔		
阿拉伯语（巴林）	ar-BH	command_and_search	True			✔		✔		
阿拉伯语（巴林）	ar-BH	default	False			✔		✔		
阿拉伯语（巴林）	ar-BH	latest_long	False	✔			✔	✔		
阿拉伯语（巴林）	ar-BH	latest_long	True	✔		✔	✔	✔		
阿拉伯语（巴林）	ar-BH	latest_short	False	✔		✔	✔	✔		
阿拉伯语（巴林）	ar-BH	latest_short	True	✔		✔	✔	✔		
阿拉伯语（埃及）	ar-EG	command_and_search	False			✔		✔		
阿拉伯语（埃及）	ar-EG	command_and_search	True			✔		✔		
阿拉伯语（埃及）	ar-EG	default	False			✔		✔		
阿拉伯语（埃及）	ar-EG	latest_long	False	✔			✔	✔		
阿拉伯语（埃及）	ar-EG	latest_long	True	✔		✔	✔	✔		
阿拉伯语（埃及）	ar-EG	latest_short	False	✔		✔	✔	✔		
阿拉伯语（埃及）	ar-EG	latest_short	True	✔		✔	✔	✔		
阿拉伯语（伊拉克）	ar-IQ	command_and_search	False			✔		✔		
阿拉伯语（伊拉克）	ar-IQ	command_and_search	True			✔		✔		
阿拉伯语（伊拉克）	ar-IQ	default	False			✔		✔		
阿拉伯语（伊拉克）	ar-IQ	latest_long	False	✔			✔	✔		
阿拉伯语（伊拉克）	ar-IQ	latest_long	True	✔		✔	✔	✔		
阿拉伯语（伊拉克）	ar-IQ	latest_short	False	✔		✔	✔	✔		
阿拉伯语（伊拉克）	ar-IQ	latest_short	True	✔		✔	✔	✔		
阿拉伯语（以色列）	ar-IL	command_and_search	False			✔		✔		
阿拉伯语（以色列）	ar-IL	command_and_search	True			✔		✔		
阿拉伯语（以色列）	ar-IL	default	False			✔		✔		
阿拉伯语（以色列）	ar-IL	latest_long	False	✔			✔	✔		
阿拉伯语（以色列）	ar-IL	latest_long	True	✔		✔	✔	✔		
阿拉伯语（以色列）	ar-IL	latest_short	False	✔		✔	✔	✔		
阿拉伯语（以色列）	ar-IL	latest_short	True	✔		✔	✔	✔		
阿拉伯语（约旦）	ar-JO	command_and_search	False			✔		✔		
阿拉伯语（约旦）	ar-JO	command_and_search	True			✔		✔		
阿拉伯语（约旦）	ar-JO	default	False			✔		✔		
阿拉伯语（约旦）	ar-JO	latest_long	False	✔			✔	✔		
阿拉伯语（约旦）	ar-JO	latest_long	True	✔		✔	✔	✔		
阿拉伯语（约旦）	ar-JO	latest_short	False	✔		✔	✔	✔		
阿拉伯语（约旦）	ar-JO	latest_short	True	✔		✔	✔	✔		
阿拉伯语（科威特）	ar-KW	command_and_search	False			✔		✔		
阿拉伯语（科威特）	ar-KW	command_and_search	True			✔		✔		
阿拉伯语（科威特）	ar-KW	default	False			✔		✔		
阿拉伯语（科威特）	ar-KW	latest_long	False	✔			✔	✔		
阿拉伯语（科威特）	ar-KW	latest_long	True	✔		✔	✔	✔		
阿拉伯语（科威特）	ar-KW	latest_short	False	✔		✔	✔	✔		
阿拉伯语（科威特）	ar-KW	latest_short	True	✔		✔	✔	✔		
阿拉伯语（黎巴嫩）	ar-LB	command_and_search	False			✔		✔		
阿拉伯语（黎巴嫩）	ar-LB	command_and_search	True			✔		✔		
阿拉伯语（黎巴嫩）	ar-LB	default	False			✔		✔		
阿拉伯语（黎巴嫩）	ar-LB	latest_long	False	✔			✔	✔		
阿拉伯语（黎巴嫩）	ar-LB	latest_long	True	✔		✔	✔	✔		
阿拉伯语（黎巴嫩）	ar-LB	latest_short	False	✔		✔	✔	✔		
阿拉伯语（黎巴嫩）	ar-LB	latest_short	True	✔		✔	✔	✔		
阿拉伯语（毛里塔尼亚）	ar-MR	command_and_search	False					✔		
阿拉伯语（毛里塔尼亚）	ar-MR	command_and_search	True					✔		
阿拉伯语（毛里塔尼亚）	ar-MR	default	False					✔		
阿拉伯语（毛里塔尼亚）	ar-MR	latest_long	False	✔			✔	✔		
阿拉伯语（毛里塔尼亚）	ar-MR	latest_long	True	✔		✔	✔	✔		
阿拉伯语（毛里塔尼亚）	ar-MR	latest_short	False	✔		✔	✔	✔		
阿拉伯语（毛里塔尼亚）	ar-MR	latest_short	True	✔		✔	✔	✔		
阿拉伯语（摩洛哥）	ar-MA	command_and_search	False					✔		
阿拉伯语（摩洛哥）	ar-MA	command_and_search	True					✔		
阿拉伯语（摩洛哥）	ar-MA	default	False					✔		
阿拉伯语（摩洛哥）	ar-MA	latest_long	False	✔			✔	✔		
阿拉伯语（摩洛哥）	ar-MA	latest_long	True	✔		✔	✔	✔		
阿拉伯语（摩洛哥）	ar-MA	latest_short	False	✔		✔	✔	✔		
阿拉伯语（摩洛哥）	ar-MA	latest_short	True	✔		✔	✔	✔		
阿拉伯语（阿曼）	ar-OM	command_and_search	False			✔		✔		
阿拉伯语（阿曼）	ar-OM	command_and_search	True			✔		✔		
阿拉伯语（阿曼）	ar-OM	default	False			✔		✔		
阿拉伯语（阿曼）	ar-OM	latest_long	False	✔			✔	✔		
阿拉伯语（阿曼）	ar-OM	latest_long	True	✔		✔	✔	✔		
阿拉伯语（阿曼）	ar-OM	latest_short	False	✔		✔	✔	✔		
阿拉伯语（阿曼）	ar-OM	latest_short	True	✔		✔	✔	✔		
阿拉伯语（卡塔尔）	ar-QA	command_and_search	False			✔		✔		
阿拉伯语（卡塔尔）	ar-QA	command_and_search	True			✔		✔		
阿拉伯语（卡塔尔）	ar-QA	default	False			✔		✔		
阿拉伯语（卡塔尔）	ar-QA	latest_long	False	✔			✔	✔		
阿拉伯语（卡塔尔）	ar-QA	latest_long	True	✔		✔	✔	✔		
阿拉伯语（卡塔尔）	ar-QA	latest_short	False	✔		✔	✔	✔		
阿拉伯语（卡塔尔）	ar-QA	latest_short	True	✔		✔	✔	✔		
阿拉伯语（沙特阿拉伯）	ar-SA	command_and_search	False			✔		✔		
阿拉伯语（沙特阿拉伯）	ar-SA	command_and_search	True			✔		✔		
阿拉伯语（沙特阿拉伯）	ar-SA	default	False			✔		✔		
阿拉伯语（沙特阿拉伯）	ar-SA	latest_long	False	✔			✔	✔		
阿拉伯语（沙特阿拉伯）	ar-SA	latest_long	True	✔		✔	✔	✔		
阿拉伯语（沙特阿拉伯）	ar-SA	latest_short	False	✔		✔	✔	✔		
阿拉伯语（沙特阿拉伯）	ar-SA	latest_short	True	✔		✔	✔	✔		
阿拉伯语（巴勒斯坦国）	ar-PS	command_and_search	False			✔		✔		
阿拉伯语（巴勒斯坦国）	ar-PS	command_and_search	True			✔		✔		
阿拉伯语（巴勒斯坦国）	ar-PS	default	False			✔		✔		
阿拉伯语（巴勒斯坦国）	ar-PS	latest_long	False	✔			✔	✔		
阿拉伯语（巴勒斯坦国）	ar-PS	latest_long	True	✔		✔	✔	✔		
阿拉伯语（巴勒斯坦国）	ar-PS	latest_short	False	✔		✔	✔	✔		
阿拉伯语（巴勒斯坦国）	ar-PS	latest_short	True	✔		✔	✔	✔		
阿拉伯语（叙利亚）	ar-SY	command_and_search	False			✔		✔		
阿拉伯语（叙利亚）	ar-SY	command_and_search	True			✔		✔		
阿拉伯语（叙利亚）	ar-SY	default	False			✔		✔		
阿拉伯语（突尼斯）	ar-TN	command_and_search	False					✔		
阿拉伯语（突尼斯）	ar-TN	command_and_search	True					✔		
阿拉伯语（突尼斯）	ar-TN	default	False					✔		
阿拉伯语（突尼斯）	ar-TN	latest_long	False	✔			✔	✔		
阿拉伯语（突尼斯）	ar-TN	latest_long	True	✔		✔	✔	✔		
阿拉伯语（突尼斯）	ar-TN	latest_short	False	✔		✔	✔	✔		
阿拉伯语（突尼斯）	ar-TN	latest_short	True	✔		✔	✔	✔		
阿拉伯语（阿拉伯联合酋长国）	ar-AE	command_and_search	False			✔		✔		
阿拉伯语（阿拉伯联合酋长国）	ar-AE	command_and_search	True			✔		✔		
阿拉伯语（阿拉伯联合酋长国）	ar-AE	default	False			✔		✔		
阿拉伯语（阿拉伯联合酋长国）	ar-AE	latest_long	False	✔			✔	✔		
阿拉伯语（阿拉伯联合酋长国）	ar-AE	latest_long	True	✔		✔	✔	✔		
阿拉伯语（阿拉伯联合酋长国）	ar-AE	latest_short	False	✔		✔	✔	✔		
阿拉伯语（阿拉伯联合酋长国）	ar-AE	latest_short	True	✔		✔	✔	✔		
阿拉伯语（也门）	ar-YE	command_and_search	False			✔		✔		
阿拉伯语（也门）	ar-YE	command_and_search	True			✔		✔		
阿拉伯语（也门）	ar-YE	default	False			✔		✔		
阿拉伯语（也门）	ar-YE	latest_long	False	✔			✔	✔		
阿拉伯语（也门）	ar-YE	latest_long	True	✔		✔	✔	✔		
阿拉伯语（也门）	ar-YE	latest_short	False	✔		✔	✔	✔		
阿拉伯语（也门）	ar-YE	latest_short	True	✔		✔	✔	✔		
亚美尼亚语（亚美尼亚）	hy-AM	command_and_search	False					✔		
亚美尼亚语（亚美尼亚）	hy-AM	command_and_search	True					✔		
亚美尼亚语（亚美尼亚）	hy-AM	default	False					✔		
阿塞拜疆语（阿塞拜疆）	az-AZ	command_and_search	False					✔		
阿塞拜疆语（阿塞拜疆）	az-AZ	command_and_search	True					✔		
阿塞拜疆语（阿塞拜疆）	az-AZ	default	False					✔		
巴斯克语（西班牙）	eu-ES	command_and_search	False					✔		
巴斯克语（西班牙）	eu-ES	command_and_search	True					✔		
巴斯克语（西班牙）	eu-ES	default	False					✔		
孟加拉语（孟加拉）	bn-BD	command_and_search	False			✔		✔		
孟加拉语（孟加拉）	bn-BD	command_and_search	True			✔		✔		
孟加拉语（孟加拉）	bn-BD	default	False			✔		✔		
孟加拉语（孟加拉）	bn-BD	latest_long	False				✔	✔		
孟加拉语（孟加拉）	bn-BD	latest_long	True			✔	✔	✔		
孟加拉语（孟加拉）	bn-BD	latest_short	False			✔	✔	✔		
孟加拉语（孟加拉）	bn-BD	latest_short	True			✔	✔	✔		
孟加拉语（印度）	bn-IN	command_and_search	False					✔		
孟加拉语（印度）	bn-IN	command_and_search	True					✔		
孟加拉语（印度）	bn-IN	default	False					✔		
波斯尼亚语（波斯尼亚和黑塞哥维那）	bs-BA	command_and_search	False					✔		
波斯尼亚语（波斯尼亚和黑塞哥维那）	bs-BA	command_and_search	True					✔		
波斯尼亚语（波斯尼亚和黑塞哥维那）	bs-BA	default	False					✔		
保加利亚语（保加利亚）	bg-BG	command_and_search	False					✔		
保加利亚语（保加利亚）	bg-BG	command_and_search	True					✔		
保加利亚语（保加利亚）	bg-BG	default	False					✔		
保加利亚语（保加利亚）	bg-BG	latest_long	False				✔	✔		
保加利亚语（保加利亚）	bg-BG	latest_long	True			✔	✔	✔		
保加利亚语（保加利亚）	bg-BG	latest_short	False			✔	✔	✔		
保加利亚语（保加利亚）	bg-BG	latest_short	True			✔	✔	✔		
缅甸语（缅甸）	my-MM	command_and_search	False					✔		
缅甸语（缅甸）	my-MM	command_and_search	True					✔		
缅甸语（缅甸）	my-MM	default	False					✔		
加泰罗尼亚语（西班牙）	ca-ES	command_and_search	False					✔		
加泰罗尼亚语（西班牙）	ca-ES	command_and_search	True					✔		
加泰罗尼亚语（西班牙）	ca-ES	default	False					✔		
简体中文（中国）	cmn-Hans-CN	command_and_search	False	✔		✔		✔		
简体中文（中国）	cmn-Hans-CN	command_and_search	True	✔		✔		✔		
简体中文（中国）	cmn-Hans-CN	default	False	✔		✔		✔		
中文（香港简体）	cmn-Hans-HK	command_and_search	False	✔		✔		✔		
中文（香港简体）	cmn-Hans-HK	command_and_search	True	✔		✔		✔		
中文（香港简体）	cmn-Hans-HK	default	False	✔		✔		✔		
中文（台湾繁体）	cmn-Hant-TW	command_and_search	False	✔		✔		✔		
中文（台湾繁体）	cmn-Hant-TW	command_and_search	True	✔		✔		✔		
中文（台湾繁体）	cmn-Hant-TW	default	False	✔		✔		✔		
中文粤语（香港繁体）	yue-Hant-HK	command_and_search	False			✔		✔		
中文粤语（香港繁体）	yue-Hant-HK	command_and_search	True			✔		✔		
中文粤语（香港繁体）	yue-Hant-HK	default	False			✔		✔		
克罗地亚语（克罗地亚）	hr-HR	command_and_search	False					✔		
克罗地亚语（克罗地亚）	hr-HR	command_and_search	True					✔		
克罗地亚语（克罗地亚）	hr-HR	default	False					✔		
捷克语（捷克共和国）	cs-CZ	command_and_search	False	✔		✔		✔	✔	
捷克语（捷克共和国）	cs-CZ	command_and_search	True	✔		✔		✔	✔	
捷克语（捷克共和国）	cs-CZ	default	False	✔		✔		✔	✔	
捷克语（捷克共和国）	cs-CZ	latest_long	False	✔			✔	✔	✔	
捷克语（捷克共和国）	cs-CZ	latest_long	True	✔		✔	✔	✔	✔	
捷克语（捷克共和国）	cs-CZ	latest_short	False	✔		✔	✔	✔	✔	
捷克语（捷克共和国）	cs-CZ	latest_short	True	✔		✔	✔	✔	✔	
丹麦语（丹麦）	da-DK	command_and_search	False	✔		✔		✔	✔	
丹麦语（丹麦）	da-DK	command_and_search	True	✔		✔		✔	✔	
丹麦语（丹麦）	da-DK	default	False	✔		✔		✔	✔	
丹麦语（丹麦）	da-DK	latest_long	False	✔		✔	✔	✔	✔	
丹麦语（丹麦）	da-DK	latest_long	True	✔			✔	✔	✔	
丹麦语（丹麦）	da-DK	latest_short	False	✔			✔	✔	✔	
丹麦语（丹麦）	da-DK	latest_short	True	✔			✔	✔	✔	
荷兰语（比利时）	nl-BE	command_and_search	False					✔	✔	
荷兰语（比利时）	nl-BE	command_and_search	True					✔	✔	
荷兰语（比利时）	nl-BE	default	False					✔	✔	
荷兰语（比利时）	nl-BE	telephony	False	✔			✔	✔	✔	
荷兰语（比利时）	nl-BE	telephony_short	False	✔		✔	✔	✔	✔	
荷兰语（荷兰）	nl-NL	command_and_search	False			✔		✔	✔	
荷兰语（荷兰）	nl-NL	command_and_search	True			✔		✔	✔	
荷兰语（荷兰）	nl-NL	default	False			✔		✔	✔	
荷兰语（荷兰）	nl-NL	latest_long	False	✔		✔	✔	✔	✔	
荷兰语（荷兰）	nl-NL	latest_long	True	✔		✔	✔	✔	✔	
荷兰语（荷兰）	nl-NL	latest_short	False	✔		✔	✔	✔	✔	
荷兰语（荷兰）	nl-NL	latest_short	True	✔		✔	✔	✔	✔	
荷兰语（荷兰）	nl-NL	telephony	False	✔			✔	✔	✔	
荷兰语（荷兰）	nl-NL	telephony	True	✔			✔	✔	✔	
荷兰语（荷兰）	nl-NL	telephony_short	False	✔		✔	✔	✔	✔	
荷兰语（荷兰）	nl-NL	telephony_short	True	✔		✔	✔	✔	✔	
英语（澳大利亚）	en-AU	command_and_search	False	✔		✔		✔	✔	✔
英语（澳大利亚）	en-AU	command_and_search	True	✔		✔		✔	✔	✔
英语（澳大利亚）	en-AU	default	False	✔		✔		✔	✔	✔
英语（澳大利亚）	en-AU	latest_long	False	✔		✔	✔	✔	✔	✔
英语（澳大利亚）	en-AU	latest_long	True	✔		✔	✔	✔	✔	✔
英语（澳大利亚）	en-AU	latest_short	False	✔		✔	✔	✔	✔	✔
英语（澳大利亚）	en-AU	latest_short	True	✔		✔	✔	✔	✔	✔
英语（澳大利亚）	en-AU	phone_call	False	✔			✔	✔		
英语（澳大利亚）	en-AU	telephony	False	✔			✔	✔	✔	✔
英语（澳大利亚）	en-AU	telephony	True	✔			✔	✔	✔	✔
英语（澳大利亚）	en-AU	telephony_short	False	✔		✔	✔	✔	✔	✔
英语（澳大利亚）	en-AU	telephony_short	True	✔		✔	✔	✔	✔	✔
英语（加拿大）	en-CA	command_and_search	False					✔	✔	✔
英语（加拿大）	en-CA	command_and_search	True					✔	✔	✔
英语（加拿大）	en-CA	default	False					✔		
英语（加拿大）	en-CA	telephony	False	✔	✔	✔	✔	✔	✔	✔
英语（加拿大）	en-CA	telephony	True	✔	✔	✔	✔	✔	✔	✔
英语（加拿大）	en-CA	telephony_short	False	✔	✔	✔	✔	✔	✔	✔
英语（加拿大）	en-CA	telephony_short	True	✔	✔	✔	✔	✔	✔	✔
英语（加纳）	en-GH	command_and_search	False			✔		✔	✔	
英语（加纳）	en-GH	command_and_search	True			✔		✔	✔	
英语（加纳）	en-GH	default	False			✔		✔	✔	
英语（香港）	en-HK	command_and_search	False					✔	✔	✔
英语（香港）	en-HK	command_and_search	True					✔	✔	✔
英语（香港）	en-HK	default	False					✔	✔	✔
英语（香港）	en-HK	telephony	False	✔			✔	✔	✔	✔
英语（香港）	en-HK	telephony_short	False	✔		✔	✔	✔	✔	✔
英语（印度）	en-IN	command_and_search	False	✔		✔		✔	✔	✔
英语（印度）	en-IN	command_and_search	True	✔		✔		✔	✔	✔
英语（印度）	en-IN	default	False	✔		✔		✔	✔	✔
英语（印度）	en-IN	latest_long	False	✔		✔	✔	✔	✔	✔
英语（印度）	en-IN	latest_long	True	✔		✔	✔	✔	✔	✔
英语（印度）	en-IN	latest_short	False	✔		✔	✔	✔	✔	✔
英语（印度）	en-IN	latest_short	True	✔		✔	✔	✔	✔	✔
英语（印度）	en-IN	telephony	False	✔			✔	✔	✔	✔
英语（印度）	en-IN	telephony	True	✔			✔	✔	✔	✔
英语（印度）	en-IN	telephony_short	False	✔		✔	✔	✔	✔	✔
英语（印度）	en-IN	telephony_short	True	✔		✔	✔	✔	✔	✔
英语（爱尔兰）	en-IE	command_and_search	False					✔	✔	✔
英语（爱尔兰）	en-IE	command_and_search	True					✔	✔	✔
英语（爱尔兰）	en-IE	default	False					✔	✔	✔
英语（爱尔兰）	en-IE	telephony	False	✔			✔	✔	✔	✔
英语（爱尔兰）	en-IE	telephony_short	False	✔		✔	✔	✔	✔	✔
英语（肯尼亚）	en-KE	command_and_search	False			✔		✔	✔	
英语（肯尼亚）	en-KE	command_and_search	True			✔		✔	✔	
英语（肯尼亚）	en-KE	default	False			✔		✔	✔	
英语（新西兰）	en-NZ	command_and_search	False					✔	✔	✔
英语（新西兰）	en-NZ	command_and_search	True					✔	✔	✔
英语（新西兰）	en-NZ	default	False					✔	✔	✔
英语（新西兰）	en-NZ	telephony	False	✔			✔	✔	✔	✔
英语（新西兰）	en-NZ	telephony_short	False	✔		✔	✔	✔	✔	✔
英语（尼日利亚）	en-NG	command_and_search	False			✔		✔	✔	
英语（尼日利亚）	en-NG	command_and_search	True			✔		✔	✔	
英语（尼日利亚）	en-NG	default	False			✔		✔	✔	
英语（巴基斯坦）	en-PK	command_and_search	False					✔	✔	✔
英语（巴基斯坦）	en-PK	command_and_search	True					✔	✔	✔
英语（巴基斯坦）	en-PK	default	False					✔	✔	✔
英语（巴基斯坦）	en-PK	telephony	False	✔			✔	✔	✔	✔
英语（巴基斯坦）	en-PK	telephony_short	False	✔		✔	✔	✔	✔	✔
英语（菲律宾）	en-PH	command_and_search	False			✔		✔		✔
英语（菲律宾）	en-PH	command_and_search	True			✔		✔		✔
英语（菲律宾）	en-PH	default	False			✔		✔		
英语（新加坡）	en-SG	command_and_search	False	✔		✔	✔	✔	✔	✔
英语（新加坡）	en-SG	command_and_search	True	✔		✔	✔	✔	✔	✔
英语（新加坡）	en-SG	default	False	✔		✔	✔	✔		
英语（新加坡）	en-SG	telephony	False	✔	✔	✔	✔	✔	✔	✔
英语（新加坡）	en-SG	telephony_short	False	✔	✔	✔	✔	✔	✔	✔
英语（南非）	en-ZA	command_and_search	False			✔		✔	✔	
英语（南非）	en-ZA	command_and_search	True			✔		✔	✔	
英语（南非）	en-ZA	default	False			✔		✔	✔	
英语（坦桑尼亚）	en-TZ	command_and_search	False			✔		✔	✔	
英语（坦桑尼亚）	en-TZ	command_and_search	True			✔		✔	✔	
英语（坦桑尼亚）	en-TZ	default	False			✔		✔	✔	
英语（英国）	en-GB	command_and_search	False	✔		✔		✔	✔	✔
英语（英国）	en-GB	command_and_search	True	✔		✔		✔	✔	✔
英语（英国）	en-GB	default	False	✔		✔		✔	✔	✔
英语（英国）	en-GB	latest_long	False	✔		✔	✔	✔	✔	✔
英语（英国）	en-GB	latest_long	True	✔		✔	✔	✔	✔	✔
英语（英国）	en-GB	latest_short	False	✔		✔	✔	✔	✔	✔
英语（英国）	en-GB	latest_short	True	✔		✔	✔	✔	✔	✔
英语（英国）	en-GB	phone_call	False	✔			✔	✔	✔	✔
英语（英国）	en-GB	telephony	False	✔			✔	✔	✔	✔
英语（英国）	en-GB	telephony	True	✔			✔	✔	✔	✔
英语（英国）	en-GB	telephony_short	False	✔		✔	✔	✔	✔	✔
英语（英国）	en-GB	telephony_short	True	✔		✔	✔	✔	✔	✔
英语（美国）	en-US	command_and_search	False	✔	✔	✔	✔	✔	✔	✔
英语（美国）	en-US	command_and_search	True	✔	✔	✔	✔	✔	✔	✔
英语（美国）	en-US	default	False	✔	✔	✔	✔	✔		
英语（美国）	en-US	latest_long	False	✔	✔	✔	✔	✔	✔	✔
英语（美国）	en-US	latest_long	True	✔	✔	✔	✔	✔	✔	✔
英语（美国）	en-US	latest_short	False	✔	✔	✔	✔	✔		✔
英语（美国）	en-US	latest_short	True	✔	✔	✔	✔	✔		✔
英语（美国）	en-US	medical_conversation	False	✔	✔		✔			
英语（美国）	en-US	medical_dictation	False	✔			✔		✔	
英语（美国）	en-US	phone_call	False	✔	✔	✔	✔	✔		
英语（美国）	en-US	telephony	False	✔	✔	✔	✔	✔	✔	✔
英语（美国）	en-US	telephony	True	✔	✔	✔	✔	✔	✔	✔
英语（美国）	en-US	telephony_short	False	✔	✔	✔	✔	✔	✔	✔
英语（美国）	en-US	telephony_short	True	✔	✔	✔	✔	✔	✔	✔
英语（美国）	en-US	video	False	✔	✔	✔	✔	✔		
爱沙尼亚语（爱沙尼亚）	et-EE	command_and_search	False					✔		
爱沙尼亚语（爱沙尼亚）	et-EE	command_and_search	True					✔		
爱沙尼亚语（爱沙尼亚）	et-EE	default	False					✔		
菲律宾语（菲律宾）	fil-PH	command_and_search	False			✔		✔		
菲律宾语（菲律宾）	fil-PH	command_and_search	True			✔		✔		
菲律宾语（菲律宾）	fil-PH	default	False			✔		✔		
芬兰语（芬兰）	fi-FI	command_and_search	False	✔		✔		✔		
芬兰语（芬兰）	fi-FI	command_and_search	True	✔		✔		✔		
芬兰语（芬兰）	fi-FI	default	False	✔		✔		✔		
芬兰语（芬兰）	fi-FI	latest_long	False	✔			✔	✔		
芬兰语（芬兰）	fi-FI	latest_long	True	✔		✔	✔	✔		
芬兰语（芬兰）	fi-FI	latest_short	False	✔		✔	✔	✔		
芬兰语（芬兰）	fi-FI	latest_short	True	✔		✔	✔	✔		
法语（比利时）	fr-BE	command_and_search	False					✔	✔	✔
法语（比利时）	fr-BE	command_and_search	True					✔	✔	✔
法语（比利时）	fr-BE	default	False					✔	✔	✔
法语（比利时）	fr-BE	telephony	False	✔			✔	✔	✔	✔
法语（比利时）	fr-BE	telephony_short	False	✔		✔		✔	✔	✔
法语（加拿大）	fr-CA	command_and_search	False			✔		✔	✔	
法语（加拿大）	fr-CA	command_and_search	True			✔		✔	✔	
法语（加拿大）	fr-CA	default	False			✔		✔	✔	
法语（加拿大）	fr-CA	latest_long	False			✔	✔		✔	
法语（加拿大）	fr-CA	latest_long	True			✔	✔		✔	
法语（加拿大）	fr-CA	latest_short	False			✔	✔	✔	✔	
法语（加拿大）	fr-CA	latest_short	True			✔	✔	✔	✔	
法语（加拿大）	fr-CA	phone_call	False				✔	✔		
法语（加拿大）	fr-CA	telephony	False				✔	✔	✔	
法语（加拿大）	fr-CA	telephony	True				✔	✔	✔	
法语（加拿大）	fr-CA	telephony_short	False			✔	✔	✔	✔	
法语（加拿大）	fr-CA	telephony_short	True			✔	✔	✔	✔	
法语（法国）	fr-FR	command_and_search	False	✔		✔		✔	✔	✔
法语（法国）	fr-FR	command_and_search	True	✔		✔		✔	✔	✔
法语（法国）	fr-FR	default	False	✔		✔		✔	✔	✔
法语（法国）	fr-FR	latest_long	False	✔		✔	✔	✔	✔	✔
法语（法国）	fr-FR	latest_long	True	✔		✔	✔	✔	✔	✔
法语（法国）	fr-FR	latest_short	False	✔		✔	✔	✔	✔	✔
法语（法国）	fr-FR	latest_short	True	✔		✔	✔	✔	✔	✔
法语（法国）	fr-FR	phone_call	False	✔			✔	✔	✔	✔
法语（法国）	fr-FR	telephony	False	✔			✔	✔	✔	✔
法语（法国）	fr-FR	telephony	True	✔			✔	✔	✔	✔
法语（法国）	fr-FR	telephony_short	False	✔		✔		✔	✔	✔
法语（法国）	fr-FR	telephony_short	True	✔		✔		✔	✔	✔
法语（瑞士）	fr-CH	command_and_search	False					✔	✔	✔
法语（瑞士）	fr-CH	command_and_search	True					✔	✔	✔
法语（瑞士）	fr-CH	default	False					✔	✔	✔
法语（瑞士）	fr-CH	telephony	False	✔			✔	✔	✔	✔
法语（瑞士）	fr-CH	telephony_short	False	✔		✔		✔	✔	✔
加利西亚语（西班牙）	gl-ES	command_and_search	False					✔		
加利西亚语（西班牙）	gl-ES	command_and_search	True					✔		
加利西亚语（西班牙）	gl-ES	default	False					✔		
格鲁吉亚语（格鲁吉亚）	ka-GE	command_and_search	False					✔		
格鲁吉亚语（格鲁吉亚）	ka-GE	command_and_search	True					✔		
格鲁吉亚语（格鲁吉亚）	ka-GE	default	False					✔		
德语（奥地利）	de-AT	command_and_search	False					✔	✔	
德语（奥地利）	de-AT	command_and_search	True					✔	✔	
德语（奥地利）	de-AT	default	False					✔	✔	
德语（奥地利）	de-AT	telephony	False	✔			✔	✔	✔	
德语（奥地利）	de-AT	telephony_short	False	✔		✔		✔	✔	
德语（德国）	de-DE	command_and_search	False	✔		✔		✔	✔	
德语（德国）	de-DE	command_and_search	True	✔		✔		✔	✔	
德语（德国）	de-DE	default	False	✔		✔		✔	✔	
德语（德国）	de-DE	latest_long	False	✔		✔	✔	✔	✔	
德语（德国）	de-DE	latest_long	True	✔		✔	✔	✔	✔	
德语（德国）	de-DE	latest_short	False	✔		✔	✔	✔	✔	
德语（德国）	de-DE	latest_short	True	✔		✔	✔	✔	✔	
德语（德国）	de-DE	phone_call	False	✔				✔	✔	
德语（德国）	de-DE	telephony	False	✔			✔	✔	✔	
德语（德国）	de-DE	telephony	True	✔			✔	✔	✔	
德语（德国）	de-DE	telephony_short	False	✔		✔		✔	✔	
德语（德国）	de-DE	telephony_short	True	✔		✔		✔	✔	
德语（瑞士）	de-CH	command_and_search	False					✔	✔	
德语（瑞士）	de-CH	command_and_search	True					✔	✔	
德语（瑞士）	de-CH	default	False					✔	✔	
德语（瑞士）	de-CH	telephony	False	✔			✔	✔	✔	
德语（瑞士）	de-CH	telephony_short	False	✔		✔		✔	✔	
希腊语（希腊）	el-GR	command_and_search	False					✔		
希腊语（希腊）	el-GR	command_and_search	True					✔		
希腊语（希腊）	el-GR	default	False					✔		
古吉拉特语（印度）	gu-IN	command_and_search	False			✔		✔		
古吉拉特语（印度）	gu-IN	command_and_search	True			✔		✔		
古吉拉特语（印度）	gu-IN	default	False			✔		✔		
希伯来语（以色列）	iw-IL	command_and_search	False			✔		✔	✔	
希伯来语（以色列）	iw-IL	command_and_search	True			✔		✔	✔	
希伯来语（以色列）	iw-IL	default	False			✔		✔	✔	
印地语（印度）	hi-IN	command_and_search	False			✔		✔	✔	
印地语（印度）	hi-IN	command_and_search	True			✔		✔	✔	
印地语（印度）	hi-IN	default	False			✔		✔	✔	
印地语（印度）	hi-IN	latest_long	False	✔			✔	✔	✔	
印地语（印度）	hi-IN	latest_long	True	✔			✔	✔	✔	
印地语（印度）	hi-IN	latest_short	False	✔		✔	✔	✔	✔	
印地语（印度）	hi-IN	latest_short	True	✔		✔	✔	✔	✔	
印地语（印度）	hi-IN	telephony	False	✔			✔	✔	✔	
印地语（印度）	hi-IN	telephony	True	✔			✔	✔	✔	
印地语（印度）	hi-IN	telephony_short	False	✔		✔	✔	✔	✔	
印地语（印度）	hi-IN	telephony_short	True	✔		✔	✔	✔	✔	
匈牙利语（匈牙利）	hu-HU	command_and_search	False					✔		
匈牙利语（匈牙利）	hu-HU	command_and_search	True					✔		
匈牙利语（匈牙利）	hu-HU	default	False					✔		
匈牙利语（匈牙利）	hu-HU	latest_long	False					✔		
匈牙利语（匈牙利）	hu-HU	latest_long	True					✔		
匈牙利语（匈牙利）	hu-HU	latest_short	False					✔		
匈牙利语（匈牙利）	hu-HU	latest_short	True					✔		
冰岛语（冰岛）	is-IS	command_and_search	False					✔		
冰岛语（冰岛）	is-IS	command_and_search	True					✔		
冰岛语（冰岛）	is-IS	default	False					✔		
印度尼西亚语（印度尼西亚）	id-ID	command_and_search	False	✔		✔		✔	✔	
印度尼西亚语（印度尼西亚）	id-ID	command_and_search	True	✔		✔		✔	✔	
印度尼西亚语（印度尼西亚）	id-ID	default	False	✔		✔		✔	✔	
印度尼西亚语（印度尼西亚）	id-ID	latest_long	False	✔			✔	✔	✔	
印度尼西亚语（印度尼西亚）	id-ID	latest_long	True	✔		✔	✔	✔	✔	
印度尼西亚语（印度尼西亚）	id-ID	latest_short	False	✔		✔	✔	✔	✔	
印度尼西亚语（印度尼西亚）	id-ID	latest_short	True	✔		✔	✔	✔	✔	
意大利语（意大利）	it-IT	command_and_search	False	✔		✔		✔	✔	
意大利语（意大利）	it-IT	command_and_search	True	✔		✔		✔	✔	
意大利语（意大利）	it-IT	default	False	✔		✔		✔	✔	
意大利语（意大利）	it-IT	latest_long	False	✔		✔	✔	✔	✔	
意大利语（意大利）	it-IT	latest_long	True	✔		✔	✔	✔	✔	
意大利语（意大利）	it-IT	latest_short	False	✔		✔	✔	✔	✔	
意大利语（意大利）	it-IT	latest_short	True	✔		✔	✔	✔	✔	
意大利语（意大利）	it-IT	phone_call	False	✔				✔	✔	
意大利语（意大利）	it-IT	telephony	False	✔			✔	✔	✔	
意大利语（意大利）	it-IT	telephony	True	✔			✔	✔	✔	
意大利语（意大利）	it-IT	telephony_short	False	✔		✔	✔	✔	✔	
意大利语（意大利）	it-IT	telephony_short	True	✔		✔	✔	✔	✔	
意大利语（瑞士）	it-CH	command_and_search	False					✔	✔	
意大利语（瑞士）	it-CH	command_and_search	True					✔	✔	
意大利语（瑞士）	it-CH	default	False					✔	✔	
意大利语（瑞士）	it-CH	telephony	False	✔			✔	✔	✔	
意大利语（瑞士）	it-CH	telephony_short	False	✔		✔	✔	✔	✔	
日语（日本）	ja-JP	command_and_search	False	✔		✔		✔	✔	
日语（日本）	ja-JP	command_and_search	True	✔		✔		✔	✔	
日语（日本）	ja-JP	default	False	✔		✔		✔	✔	
日语（日本）	ja-JP	latest_long	False	✔		✔	✔	✔	✔	
日语（日本）	ja-JP	latest_long	True	✔		✔	✔	✔	✔	
日语（日本）	ja-JP	latest_short	False	✔		✔	✔	✔	✔	
日语（日本）	ja-JP	latest_short	True	✔		✔	✔	✔	✔	
日语（日本）	ja-JP	phone_call	False	✔			✔	✔	✔	
日语（日本）	ja-JP	telephony	False	✔			✔	✔	✔	
日语（日本）	ja-JP	telephony	True	✔			✔	✔	✔	
日语（日本）	ja-JP	telephony_short	False	✔		✔	✔	✔	✔	
日语（日本）	ja-JP	telephony_short	True	✔		✔	✔	✔	✔	
爪哇语（印度尼西亚）	jv-ID	command_and_search	False					✔		
爪哇语（印度尼西亚）	jv-ID	command_and_search	True					✔		
爪哇语（印度尼西亚）	jv-ID	default	False					✔		
卡纳达语（印度）	kn-IN	command_and_search	False			✔		✔		
卡纳达语（印度）	kn-IN	command_and_search	True			✔		✔		
卡纳达语（印度）	kn-IN	default	False			✔		✔		
卡纳达语（印度）	kn-IN	latest_long	False				✔	✔		
卡纳达语（印度）	kn-IN	latest_long	True			✔	✔	✔		
卡纳达语（印度）	kn-IN	latest_short	False			✔	✔	✔		
卡纳达语（印度）	kn-IN	latest_short	True			✔	✔	✔		
哈萨克语（哈萨克斯坦）	kk-KZ	command_and_search	False					✔		
哈萨克语（哈萨克斯坦）	kk-KZ	command_and_search	True					✔		
哈萨克语（哈萨克斯坦）	kk-KZ	default	False					✔		
高棉语（柬埔寨）	km-KH	command_and_search	False					✔		
高棉语（柬埔寨）	km-KH	command_and_search	True					✔		
高棉语（柬埔寨）	km-KH	default	False					✔		
高棉语（柬埔寨）	km-KH	latest_long	False				✔	✔		
高棉语（柬埔寨）	km-KH	latest_long	True				✔	✔		
高棉语（柬埔寨）	km-KH	latest_short	False				✔	✔		
高棉语（柬埔寨）	km-KH	latest_short	True				✔	✔		
卢旺达语（卢旺达）	rw-RW	latest_long	False					✔		
卢旺达语（卢旺达）	rw-RW	latest_long	True					✔		
卢旺达语（卢旺达）	rw-RW	latest_short	False					✔		
卢旺达语（卢旺达）	rw-RW	latest_short	True					✔		
韩语（韩国）	ko-KR	command_and_search	False	✔		✔		✔	✔	
韩语（韩国）	ko-KR	command_and_search	True	✔		✔		✔	✔	
韩语（韩国）	ko-KR	default	False	✔		✔		✔	✔	
韩语（韩国）	ko-KR	latest_long	False	✔			✔	✔	✔	
韩语（韩国）	ko-KR	latest_long	True	✔		✔	✔	✔	✔	
韩语（韩国）	ko-KR	latest_short	False	✔		✔	✔	✔	✔	
韩语（韩国）	ko-KR	latest_short	True	✔		✔	✔	✔	✔	
韩语（韩国）	ko-KR	telephony	False	✔			✔	✔	✔	
韩语（韩国）	ko-KR	telephony	True	✔			✔	✔	✔	
韩语（韩国）	ko-KR	telephony_short	False	✔			✔	✔	✔	
韩语（韩国）	ko-KR	telephony_short	True	✔			✔	✔	✔	
老挝语（老挝）	lo-LA	command_and_search	False					✔		
老挝语（老挝）	lo-LA	command_and_search	True					✔		
老挝语（老挝）	lo-LA	default	False					✔		
拉脱维亚语（拉脱维亚）	lv-LV	command_and_search	False					✔		
拉脱维亚语（拉脱维亚）	lv-LV	command_and_search	True					✔		
拉脱维亚语（拉脱维亚）	lv-LV	default	False					✔		
立陶宛语（立陶宛）	lt-LT	command_and_search	False					✔		
立陶宛语（立陶宛）	lt-LT	command_and_search	True					✔		
立陶宛语（立陶宛）	lt-LT	default	False					✔		
马其顿语（北马其顿）	mk-MK	command_and_search	False					✔		
马其顿语（北马其顿）	mk-MK	command_and_search	True					✔		
马其顿语（北马其顿）	mk-MK	default	False					✔		
马其顿语（北马其顿）	mk-MK	latest_long	False					✔		
马其顿语（北马其顿）	mk-MK	latest_long	True					✔		
马其顿语（北马其顿）	mk-MK	latest_short	False					✔		
马其顿语（北马其顿）	mk-MK	latest_short	True					✔		
马来语（马来西亚）	ms-MY	command_and_search	False			✔		✔		
马来语（马来西亚）	ms-MY	command_and_search	True			✔		✔		
马来语（马来西亚）	ms-MY	default	False			✔		✔		
马拉雅拉姆语（印度）	ml-IN	command_and_search	False			✔		✔	✔	
马拉雅拉姆语（印度）	ml-IN	command_and_search	True			✔		✔	✔	
马拉雅拉姆语（印度）	ml-IN	default	False			✔		✔	✔	
马拉雅拉姆语（印度）	ml-IN	latest_long	False				✔	✔	✔	
马拉雅拉姆语（印度）	ml-IN	latest_long	True			✔	✔	✔	✔	
马拉雅拉姆语（印度）	ml-IN	latest_short	False			✔	✔	✔	✔	
马拉雅拉姆语（印度）	ml-IN	latest_short	True			✔	✔	✔	✔	
马拉地语（印度）	mr-IN	command_and_search	False			✔		✔		
马拉地语（印度）	mr-IN	command_and_search	True			✔		✔		
马拉地语（印度）	mr-IN	default	False			✔		✔		
马拉地语（印度）	mr-IN	latest_long	False				✔	✔		
马拉地语（印度）	mr-IN	latest_long	True			✔	✔	✔		
马拉地语（印度）	mr-IN	latest_short	False			✔	✔	✔		
马拉地语（印度）	mr-IN	latest_short	True			✔	✔	✔		
蒙古语（蒙古）	mn-MN	command_and_search	False					✔		
蒙古语（蒙古）	mn-MN	command_and_search	True					✔		
蒙古语（蒙古）	mn-MN	default	False					✔		
尼泊尔语（尼泊尔）	ne-NP	command_and_search	False					✔		
尼泊尔语（尼泊尔）	ne-NP	command_and_search	True					✔		
尼泊尔语（尼泊尔）	ne-NP	default	False					✔		
博克马尔挪威语（挪威）	no-NO	command_and_search	False			✔		✔	✔	
博克马尔挪威语（挪威）	no-NO	command_and_search	True			✔		✔	✔	
博克马尔挪威语（挪威）	no-NO	default	False			✔		✔	✔	
博克马尔挪威语（挪威）	no-NO	latest_long	False				✔	✔	✔	
博克马尔挪威语（挪威）	no-NO	latest_long	True			✔	✔	✔	✔	
博克马尔挪威语（挪威）	no-NO	latest_short	False			✔	✔	✔	✔	
博克马尔挪威语（挪威）	no-NO	latest_short	True			✔	✔	✔	✔	
波斯语（伊朗）	fa-IR	command_and_search	False			✔		✔		
波斯语（伊朗）	fa-IR	command_and_search	True			✔		✔		
波斯语（伊朗）	fa-IR	default	False			✔		✔		
波兰语（波兰）	pl-PL	command_and_search	False			✔		✔	✔	
波兰语（波兰）	pl-PL	command_and_search	True			✔		✔	✔	
波兰语（波兰）	pl-PL	default	False			✔		✔	✔	
波兰语（波兰）	pl-PL	latest_long	False				✔	✔	✔	
波兰语（波兰）	pl-PL	latest_long	True			✔	✔	✔	✔	
波兰语（波兰）	pl-PL	latest_short	False			✔	✔	✔	✔	
波兰语（波兰）	pl-PL	latest_short	True			✔	✔	✔	✔	
葡萄牙语（巴西）	pt-BR	command_and_search	False			✔		✔	✔	
葡萄牙语（巴西）	pt-BR	command_and_search	True			✔		✔	✔	
葡萄牙语（巴西）	pt-BR	default	False			✔		✔	✔	
葡萄牙语（巴西）	pt-BR	latest_long	False	✔		✔	✔	✔	✔	
葡萄牙语（巴西）	pt-BR	latest_long	True	✔		✔	✔	✔	✔	
葡萄牙语（巴西）	pt-BR	latest_short	False	✔		✔	✔	✔	✔	
葡萄牙语（巴西）	pt-BR	latest_short	True	✔		✔	✔	✔	✔	
葡萄牙语（巴西）	pt-BR	phone_call	False	✔				✔	✔	
葡萄牙语（巴西）	pt-BR	telephony	False	✔			✔	✔	✔	
葡萄牙语（巴西）	pt-BR	telephony	True	✔			✔	✔	✔	
葡萄牙语（巴西）	pt-BR	telephony_short	False	✔		✔	✔	✔	✔	
葡萄牙语（巴西）	pt-BR	telephony_short	True	✔		✔	✔	✔	✔	
葡萄牙语（葡萄牙）	pt-PT	command_and_search	False			✔		✔	✔	
葡萄牙语（葡萄牙）	pt-PT	command_and_search	True			✔		✔	✔	
葡萄牙语（葡萄牙）	pt-PT	default	False			✔		✔	✔	
葡萄牙语（葡萄牙）	pt-PT	latest_long	False				✔	✔	✔	
葡萄牙语（葡萄牙）	pt-PT	latest_long	True			✔	✔	✔	✔	
葡萄牙语（葡萄牙）	pt-PT	latest_short	False			✔	✔	✔	✔	
葡萄牙语（葡萄牙）	pt-PT	latest_short	True			✔	✔	✔	✔	
葡萄牙语（葡萄牙）	pt-PT	telephony	False				✔	✔	✔	
葡萄牙语（葡萄牙）	pt-PT	telephony	True				✔	✔	✔	
葡萄牙语（葡萄牙）	pt-PT	telephony_short	False				✔	✔	✔	
葡萄牙语（葡萄牙）	pt-PT	telephony_short	True				✔	✔	✔	
旁遮普语（果鲁穆奇语，印度）	pa-Guru-IN	command_and_search	False					✔		
旁遮普语（果鲁穆奇语，印度）	pa-Guru-IN	command_and_search	True					✔		
旁遮普语（果鲁穆奇语，印度）	pa-Guru-IN	default	False					✔		
罗马尼亚语（罗马尼亚）	ro-RO	command_and_search	False					✔		
罗马尼亚语（罗马尼亚）	ro-RO	command_and_search	True					✔		
罗马尼亚语（罗马尼亚）	ro-RO	default	False					✔		
罗马尼亚语（罗马尼亚）	ro-RO	latest_long	False				✔	✔		
罗马尼亚语（罗马尼亚）	ro-RO	latest_long	True			✔	✔	✔		
罗马尼亚语（罗马尼亚）	ro-RO	latest_short	False			✔	✔	✔		
罗马尼亚语（罗马尼亚）	ro-RO	latest_short	True			✔	✔	✔		
俄语（俄罗斯）	ru-RU	command_and_search	False			✔		✔	✔	
俄语（俄罗斯）	ru-RU	command_and_search	True			✔		✔	✔	
俄语（俄罗斯）	ru-RU	default	False			✔		✔	✔	
俄语（俄罗斯）	ru-RU	latest_long	False	✔			✔	✔	✔	
俄语（俄罗斯）	ru-RU	latest_long	True	✔		✔	✔	✔	✔	
俄语（俄罗斯）	ru-RU	latest_short	False	✔		✔	✔	✔	✔	
俄语（俄罗斯）	ru-RU	latest_short	True	✔		✔	✔	✔	✔	
俄语（俄罗斯）	ru-RU	phone_call	False	✔				✔	✔	
塞尔维亚语（塞尔维亚）	sr-RS	command_and_search	False			✔		✔		
塞尔维亚语（塞尔维亚）	sr-RS	command_and_search	True			✔		✔		
塞尔维亚语（塞尔维亚）	sr-RS	default	False			✔		✔		
僧伽罗语（斯里兰卡）	si-LK	command_and_search	False					✔		
僧伽罗语（斯里兰卡）	si-LK	command_and_search	True					✔		
僧伽罗语（斯里兰卡）	si-LK	default	False					✔		
斯洛伐克语（斯洛伐克）	sk-SK	command_and_search	False					✔		
斯洛伐克语（斯洛伐克）	sk-SK	command_and_search	True					✔		
斯洛伐克语（斯洛伐克）	sk-SK	default	False					✔		
斯洛文尼亚语（斯洛文尼亚）	sl-SI	command_and_search	False					✔		
斯洛文尼亚语（斯洛文尼亚）	sl-SI	command_and_search	True					✔		
斯洛文尼亚语（斯洛文尼亚）	sl-SI	default	False					✔		
南索托语（南非）	st-ZA	latest_long	False					✔		
南索托语（南非）	st-ZA	latest_long	True					✔		
南索托语（南非）	st-ZA	latest_short	False					✔		
南索托语（南非）	st-ZA	latest_short	True					✔		
西班牙语（阿根廷）	es-AR	command_and_search	False					✔	✔	
西班牙语（阿根廷）	es-AR	command_and_search	True					✔	✔	
西班牙语（阿根廷）	es-AR	default	False					✔	✔	
西班牙语（阿根廷）	es-AR	telephony_short	False	✔		✔	✔	✔	✔	
西班牙语（玻利维亚）	es-BO	command_and_search	False					✔	✔	
西班牙语（玻利维亚）	es-BO	command_and_search	True					✔	✔	
西班牙语（玻利维亚）	es-BO	default	False					✔	✔	
西班牙语（玻利维亚）	es-BO	telephony_short	False	✔		✔	✔	✔	✔	
西班牙语（智利）	es-CL	command_and_search	False					✔	✔	
西班牙语（智利）	es-CL	command_and_search	True					✔	✔	
西班牙语（智利）	es-CL	default	False					✔	✔	
西班牙语（智利）	es-CL	telephony_short	False	✔		✔	✔	✔	✔	
西班牙语（哥伦比亚）	es-CO	command_and_search	False					✔	✔	
西班牙语（哥伦比亚）	es-CO	command_and_search	True					✔	✔	
西班牙语（哥伦比亚）	es-CO	default	False					✔	✔	
西班牙语（哥伦比亚）	es-CO	telephony_short	False	✔		✔	✔	✔	✔	
西班牙语（哥斯达黎加）	es-CR	command_and_search	False					✔	✔	
西班牙语（哥斯达黎加）	es-CR	command_and_search	True					✔	✔	
西班牙语（哥斯达黎加）	es-CR	default	False					✔	✔	
西班牙语（哥斯达黎加）	es-CR	telephony_short	False	✔		✔	✔	✔	✔	
西班牙语（多米尼加共和国）	es-DO	command_and_search	False					✔	✔	
西班牙语（多米尼加共和国）	es-DO	command_and_search	True					✔	✔	
西班牙语（多米尼加共和国）	es-DO	default	False					✔	✔	
西班牙语（多米尼加共和国）	es-DO	telephony_short	False	✔		✔	✔	✔	✔	
西班牙语（厄瓜多尔）	es-EC	command_and_search	False					✔	✔	
西班牙语（厄瓜多尔）	es-EC	command_and_search	True					✔	✔	
西班牙语（厄瓜多尔）	es-EC	default	False					✔	✔	
西班牙语（厄瓜多尔）	es-EC	telephony_short	False	✔		✔	✔	✔	✔	
西班牙语（萨尔瓦多）	es-SV	command_and_search	False					✔	✔	
西班牙语（萨尔瓦多）	es-SV	command_and_search	True					✔	✔	
西班牙语（萨尔瓦多）	es-SV	default	False					✔	✔	
西班牙语（萨尔瓦多）	es-SV	telephony_short	False	✔		✔	✔	✔	✔	
西班牙语（危地马拉）	es-GT	command_and_search	False					✔	✔	
西班牙语（危地马拉）	es-GT	command_and_search	True					✔	✔	
西班牙语（危地马拉）	es-GT	default	False					✔	✔	
西班牙语（危地马拉）	es-GT	telephony_short	False	✔		✔	✔	✔	✔	
西班牙语（洪都拉斯）	es-HN	command_and_search	False					✔	✔	
西班牙语（洪都拉斯）	es-HN	command_and_search	True					✔	✔	
西班牙语（洪都拉斯）	es-HN	default	False					✔	✔	
西班牙语（洪都拉斯）	es-HN	telephony_short	False	✔		✔	✔	✔	✔	
西班牙语（墨西哥）	es-MX	command_and_search	False					✔	✔	
西班牙语（墨西哥）	es-MX	command_and_search	True					✔	✔	
西班牙语（墨西哥）	es-MX	default	False					✔	✔	
西班牙语（墨西哥）	es-MX	telephony_short	False	✔		✔	✔	✔	✔	
西班牙语（尼加拉瓜）	es-NI	command_and_search	False					✔	✔	
西班牙语（尼加拉瓜）	es-NI	command_and_search	True					✔	✔	
西班牙语（尼加拉瓜）	es-NI	default	False					✔	✔	
西班牙语（尼加拉瓜）	es-NI	telephony_short	False	✔		✔	✔	✔	✔	
西班牙语（巴拿马）	es-PA	command_and_search	False					✔	✔	
西班牙语（巴拿马）	es-PA	command_and_search	True					✔	✔	
西班牙语（巴拿马）	es-PA	default	False					✔	✔	
西班牙语（巴拿马）	es-PA	telephony_short	False	✔		✔	✔	✔	✔	
西班牙语（巴拉圭）	es-PY	command_and_search	False					✔	✔	
西班牙语（巴拉圭）	es-PY	command_and_search	True					✔	✔	
西班牙语（巴拉圭）	es-PY	default	False					✔	✔	
西班牙语（秘鲁）	es-PE	command_and_search	False					✔	✔	
西班牙语（秘鲁）	es-PE	command_and_search	True					✔	✔	
西班牙语（秘鲁）	es-PE	default	False					✔	✔	
西班牙语（秘鲁）	es-PE	telephony_short	False	✔		✔	✔	✔	✔	
西班牙语（波多黎各）	es-PR	command_and_search	False					✔	✔	
西班牙语（波多黎各）	es-PR	command_and_search	True					✔	✔	
西班牙语（波多黎各）	es-PR	default	False					✔	✔	
西班牙语（波多黎各）	es-PR	telephony_short	False	✔		✔	✔	✔	✔	
西班牙语（西班牙）	es-ES	command_and_search	False			✔		✔	✔	
西班牙语（西班牙）	es-ES	command_and_search	True			✔		✔	✔	
西班牙语（西班牙）	es-ES	default	False			✔		✔	✔	
西班牙语（西班牙）	es-ES	latest_long	False	✔		✔	✔	✔	✔	
西班牙语（西班牙）	es-ES	latest_long	True	✔		✔	✔	✔	✔	
西班牙语（西班牙）	es-ES	latest_short	False	✔		✔	✔	✔	✔	
西班牙语（西班牙）	es-ES	latest_short	True	✔		✔	✔	✔	✔	
西班牙语（西班牙）	es-ES	phone_call	False				✔	✔	✔	
西班牙语（西班牙）	es-ES	telephony	False	✔			✔	✔	✔	
西班牙语（西班牙）	es-ES	telephony	True	✔			✔	✔	✔	
西班牙语（西班牙）	es-ES	telephony_short	False	✔		✔	✔	✔	✔	
西班牙语（西班牙）	es-ES	telephony_short	True	✔		✔	✔	✔	✔	
西班牙语（美国）	es-US	command_and_search	False	✔		✔		✔	✔	
西班牙语（美国）	es-US	command_and_search	True	✔		✔		✔	✔	
西班牙语（美国）	es-US	default	False	✔		✔		✔	✔	
西班牙语（美国）	es-US	latest_long	False	✔		✔	✔	✔	✔	
西班牙语（美国）	es-US	latest_long	True	✔		✔	✔	✔	✔	
西班牙语（美国）	es-US	latest_short	False	✔		✔	✔	✔	✔	
西班牙语（美国）	es-US	latest_short	True	✔		✔	✔	✔	✔	
西班牙语（美国）	es-US	phone_call	False	✔			✔	✔	✔	
西班牙语（美国）	es-US	telephony	True	✔			✔	✔	✔	
西班牙语（美国）	es-US	telephony_short	False	✔		✔	✔	✔	✔	
西班牙语（美国）	es-US	telephony_short	True	✔		✔	✔	✔	✔	
西班牙语（乌拉圭）	es-UY	command_and_search	False					✔	✔	
西班牙语（乌拉圭）	es-UY	command_and_search	True					✔	✔	
西班牙语（乌拉圭）	es-UY	default	False					✔	✔	
西班牙语（乌拉圭）	es-UY	telephony_short	False	✔		✔	✔	✔	✔	
西班牙语（委内瑞拉）	es-VE	command_and_search	False					✔	✔	
西班牙语（委内瑞拉）	es-VE	command_and_search	True					✔	✔	
西班牙语（委内瑞拉）	es-VE	default	False					✔	✔	
西班牙语（委内瑞拉）	es-VE	telephony_short	False	✔		✔	✔	✔	✔	
巽他语（印度尼西亚）	su-ID	command_and_search	False					✔		
巽他语（印度尼西亚）	su-ID	command_and_search	True					✔		
巽他语（印度尼西亚）	su-ID	default	False					✔		
斯瓦希里语（肯尼亚）	sw-KE	command_and_search	False					✔		
斯瓦希里语（肯尼亚）	sw-KE	command_and_search	True					✔		
斯瓦希里语（肯尼亚）	sw-KE	default	False					✔		
斯瓦希里语（坦桑尼亚）	sw-TZ	command_and_search	False					✔		
斯瓦希里语（坦桑尼亚）	sw-TZ	command_and_search	True					✔		
斯瓦希里语（坦桑尼亚）	sw-TZ	default	False					✔		
斯威士语（拉丁字母，南非）	ss-Latn-ZA	latest_long	False					✔		
斯威士语（拉丁字母，南非）	ss-Latn-ZA	latest_long	True					✔		
斯威士语（拉丁字母，南非）	ss-Latn-ZA	latest_short	False					✔		
斯威士语（拉丁字母，南非）	ss-Latn-ZA	latest_short	True					✔		
瑞典语（瑞典）	sv-SE	command_and_search	False	✔		✔		✔	✔	
瑞典语（瑞典）	sv-SE	command_and_search	True	✔		✔		✔	✔	
瑞典语（瑞典）	sv-SE	default	False	✔		✔		✔	✔	
瑞典语（瑞典）	sv-SE	latest_long	False	✔			✔	✔	✔	
瑞典语（瑞典）	sv-SE	latest_long	True	✔		✔	✔	✔	✔	
瑞典语（瑞典）	sv-SE	latest_short	False	✔		✔	✔	✔	✔	
瑞典语（瑞典）	sv-SE	latest_short	True	✔		✔	✔	✔	✔	
泰米尔语（印度）	ta-IN	command_and_search	False			✔		✔		
泰米尔语（印度）	ta-IN	command_and_search	True			✔		✔		
泰米尔语（印度）	ta-IN	default	False			✔		✔		
泰米尔语（印度）	ta-IN	latest_long	False				✔	✔		
泰米尔语（印度）	ta-IN	latest_long	True			✔	✔	✔		
泰米尔语（印度）	ta-IN	latest_short	False			✔	✔	✔		
泰米尔语（印度）	ta-IN	latest_short	True			✔	✔	✔		
泰米尔语（马来西亚）	ta-MY	command_and_search	False					✔		
泰米尔语（马来西亚）	ta-MY	command_and_search	True					✔		
泰米尔语（马来西亚）	ta-MY	default	False					✔		
泰米尔语（新加坡）	ta-SG	command_and_search	False					✔		
泰米尔语（新加坡）	ta-SG	command_and_search	True					✔		
泰米尔语（新加坡）	ta-SG	default	False					✔		
泰米尔语（斯里兰卡）	ta-LK	command_and_search	False					✔		
泰米尔语（斯里兰卡）	ta-LK	command_and_search	True					✔		
泰米尔语（斯里兰卡）	ta-LK	default	False					✔		
泰卢固语（印度）	te-IN	command_and_search	False			✔		✔		
泰卢固语（印度）	te-IN	command_and_search	True			✔		✔		
泰卢固语（印度）	te-IN	default	False			✔		✔		
泰卢固语（印度）	te-IN	latest_long	False				✔	✔		
泰卢固语（印度）	te-IN	latest_long	True			✔	✔	✔		
泰卢固语（印度）	te-IN	latest_short	False			✔	✔	✔		
泰卢固语（印度）	te-IN	latest_short	True			✔	✔	✔		
泰语（泰国）	th-TH	command_and_search	False			✔		✔		
泰语（泰国）	th-TH	command_and_search	True			✔		✔		
泰语（泰国）	th-TH	default	False			✔		✔		
泰语（泰国）	th-TH	latest_long	False				✔	✔		
泰语（泰国）	th-TH	latest_long	True			✔	✔	✔		
泰语（泰国）	th-TH	latest_short	False			✔	✔	✔		
泰语（泰国）	th-TH	latest_short	True			✔	✔	✔		
聪加语（南非）	ts-ZA	latest_long	False					✔		
聪加语（南非）	ts-ZA	latest_long	True					✔		
聪加语（南非）	ts-ZA	latest_short	False					✔		
聪加语（南非）	ts-ZA	latest_short	True					✔		
茨瓦纳语（拉丁字母，南非）	tn-Latn-ZA	latest_long	False					✔		
茨瓦纳语（拉丁字母，南非）	tn-Latn-ZA	latest_long	True					✔		
茨瓦纳语（拉丁字母，南非）	tn-Latn-ZA	latest_short	False					✔		
茨瓦纳语（拉丁字母，南非）	tn-Latn-ZA	latest_short	True					✔		
土耳其语（土耳其）	tr-TR	command_and_search	False	✔		✔		✔	✔	
土耳其语（土耳其）	tr-TR	command_and_search	True	✔		✔		✔	✔	
土耳其语（土耳其）	tr-TR	default	False	✔		✔		✔	✔	
土耳其语（土耳其）	tr-TR	latest_long	False	✔			✔	✔	✔	
土耳其语（土耳其）	tr-TR	latest_long	True	✔		✔	✔	✔	✔	
土耳其语（土耳其）	tr-TR	latest_short	False	✔		✔	✔	✔	✔	
土耳其语（土耳其）	tr-TR	latest_short	True	✔		✔	✔	✔	✔	
乌克兰语（乌克兰）	uk-UA	command_and_search	False			✔		✔		
乌克兰语（乌克兰）	uk-UA	command_and_search	True			✔		✔		
乌克兰语（乌克兰）	uk-UA	default	False			✔		✔		
乌克兰语（乌克兰）	uk-UA	latest_long	False				✔	✔		
乌克兰语（乌克兰）	uk-UA	latest_long	True			✔	✔	✔		
乌克兰语（乌克兰）	uk-UA	latest_short	False			✔	✔	✔		
乌克兰语（乌克兰）	uk-UA	latest_short	True			✔	✔	✔		
乌尔都语（印度）	ur-IN	command_and_search	False					✔		
乌尔都语（印度）	ur-IN	command_and_search	True					✔		
乌尔都语（印度）	ur-IN	default	False					✔		
乌尔都语（巴基斯坦）	ur-PK	command_and_search	False			✔		✔		
乌尔都语（巴基斯坦）	ur-PK	command_and_search	True			✔		✔		
乌尔都语（巴基斯坦）	ur-PK	default	False			✔		✔		
乌兹别克语（乌兹别克斯坦）	uz-UZ	command_and_search	False					✔		
乌兹别克语（乌兹别克斯坦）	uz-UZ	command_and_search	True					✔		
乌兹别克语（乌兹别克斯坦）	uz-UZ	default	False					✔		
文达语（南非）	ve-ZA	latest_long	False					✔		
文达语（南非）	ve-ZA	latest_long	True					✔		
文达语（南非）	ve-ZA	latest_short	False					✔		
文达语（南非）	ve-ZA	latest_short	True					✔		
越南语（越南）	vi-VN	command_and_search	False			✔		✔		
越南语（越南）	vi-VN	command_and_search	True			✔		✔		
越南语（越南）	vi-VN	default	False			✔		✔		
越南语（越南）	vi-VN	latest_long	False	✔			✔	✔		
越南语（越南）	vi-VN	latest_long	True	✔		✔	✔	✔		
越南语（越南）	vi-VN	latest_short	False	✔		✔	✔	✔		
越南语（越南）	vi-VN	latest_short	True	✔		✔	✔	✔		
科萨语（南非）	xh-ZA	latest_long	False					✔		
科萨语（南非）	xh-ZA	latest_long	True					✔		
科萨语（南非）	xh-ZA	latest_short	False					✔		
科萨语（南非）	xh-ZA	latest_short	True					✔		
祖鲁语（南非）	zu-ZA	command_and_search	False			✔		✔		
祖鲁语（南非）	zu-ZA	command_and_search	True			✔		✔		
祖鲁语（南非）	zu-ZA	default	False			✔		✔	