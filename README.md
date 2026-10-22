# Better Info Mod · macOS 1.3.8

为《英雄连2》Feral Mac 版 1.3.8（build 306362.56045）校正英文数值说明；当前修正180条，只修改显示文字，不改变游戏属性。

## 文件

- `macos/RelicCoH2.English.ucs`：可安装的 Mac 英文校正版。
- `data/macos-1.3.8.json`：校正前后文字、本机属性证据、版本与哈希、待确认条目。
- `tools/`：校正版生成、验证与 SGA v7 属性提取工具。
- `tests/`：本地化文件完整性检查。
- 根目录 `.ucs`：上游文件；英文和德文同步正式 v1.2 发布包。其他语言保持上游状态，尚未校正。
- `src/`：上游保留的原始本地化文件。

## 安装

退出游戏，在 Steam 中浏览《英雄连2》的本地文件，进入 `CompanyOfHeroes2Data/coh2/locale/english/`。先备份该目录中的 `reliccoh2.english.ucs`，再用本仓库 `macos/RelicCoH2.English.ucs` 替换它，保持目标文件名。

本版本面向 Mac 原生版原版多人规则。战役、战区、改变平衡的模组、Windows/Wine 版和其他语言不在已核对范围。待确认项详见校正清单；没有进行游戏内逐项实测。

## 生成与验证

需要 Python 3，无额外 Python 依赖。

```sh
python3 tools/build_macos.py
python3 tools/build_macos.py --check
python3 -m unittest discover -s tests
```

需要重新读取本机属性时，从 [CoH2 Stats 使用的 RGDTools 包](https://raw.githubusercontent.com/cohstats/coh2stats/master/scripts/RGDTools_v1.3.7z) 提取 `hash_dict.txt`，再运行：

```sh
python3 tools/extract_mac_attributes.py /path/to/attribarchive.sga /tmp/attributes.json --hash-dictionary /path/to/hash_dict.txt
```

工具只读 SGA，验证存储数据 CRC 和解压长度，并保留未知字段及重复数组项。不要把游戏属性完整导出或第三方字典提交到仓库。

## 来源与致谢

基于 [Mithiriath/coh2_better-info-mod](https://github.com/Mithiriath/coh2_better-info-mod) 的 [v1.2 正式发布包](https://github.com/Mithiriath/coh2_better-info-mod/releases/tag/v1.2)。感谢 Mithiriath、jamesjamozo、Elpern、Osinyagov 及原 Numerical Veterancy Description Mod 的 Sarantini、CookiezNcreem、Tobis、Harold、RussianHamster、Karotten Harry、3nder990。

版本范围参考 [Feral 官方 Mac 更新说明](https://steamcommunity.com/app/231430/discussions/0/3040481757531253611/)；数值以该版本本机 `attribarchive.sga` 为依据。
