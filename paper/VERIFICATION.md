# Citation verification log (step A2, extended after review round 1)

Rule: a reference enters `refs.bib` only if title, authors (at least the verified prefix),
venue, and year were confirmed against an authoritative record. Where the full author list
could not be confirmed from the record, the entry uses "and others" after the verified prefix.
Verified 2026-10-10. DBLP's API was behind a bot-check wall that day; Crossref, PMLR, and the
arXiv API were used instead.

| Key | Source checked | Record |
|---|---|---|
| weiser1984 | Crossref DOI 10.1109/TSE.1984.5010248 | IEEE TSE SE-10(4), 352–357, 1984 |
| horwitz1990 | Crossref DOI 10.1145/77606.77608 | ACM TOPLAS 12(1), 26–60, 1990 |
| binkley2014orbs | Crossref DOI 10.1145/2635868.2635893 | FSE 2014, 109–120 |
| ohearn2001local | Crossref DOI 10.1007/3-540-44802-0_1 | CSL 2001, LNCS 2142, 1–19 |
| borgida1995frame | Crossref DOI 10.1109/32.469460 | IEEE TSE 21(10), 785–798, 1995 |
| rothermel1997safe | Crossref DOI 10.1145/248233.248262 | ACM TOSEM 6(2), 173–210, 1997 |
| ren2004chianti | Crossref DOI 10.1145/1028976.1029012 | OOPSLA 2004, 432–448 (Ren, Shah, Tip, Ryder, Chesley) |
| bairi2024codeplan | Crossref DOI 10.1145/3643757 | PACMSE 1(FSE), 675–698, 2024 |
| zhang2023repocoder | Crossref DOI 10.18653/v1/2023.emnlp-main.151 | EMNLP 2023, 2471–2484 |
| xia2025agentless | Crossref DOI 10.1145/3715754 | PACMSE 2(FSE), 801–824, 2025. Published title drops the arXiv "Agentless:" prefix |
| liu2024lost | Crossref DOI 10.1162/tacl_a_00638 | TACL 12, 157–173, 2024 |
| shrivastava2023repo | PMLR page v202/shrivastava23a | ICML 2023, PMLR 202:31693–31715 |
| shi2023distracted | PMLR page v202/shi23a | ICML 2023, PMLR 202:31210–31227 |
| joren2024sufficient | arXiv API 2411.06037 | title and first three authors confirmed; venue not asserted |
| zeller2002simplifying | Crossref DOI 10.1109/32.988498 | IEEE TSE 28(2), 183–200, 2002 |
| blackwell1953equivalent | Crossref DOI 10.1214/aoms/1177729032 | Ann. Math. Statist. 24(2), 265–272, 1953 |
| good1967total | Crossref DOI 10.1093/bjps/17.4.319 | BJPS 17(4), 319–321, 1967 |
| lecam1964sufficiency | Crossref DOI 10.1214/aoms/1177700372 | Ann. Math. Statist. 35(4), 1419–1455, 1964 |
| deyoung2020eraser | Crossref DOI 10.18653/v1/2020.acl-main.408 | ACL 2020, 4443–4458; first four authors confirmed |
| cuconasu2024noise | Crossref DOI 10.1145/3626772.3657834 | SIGIR 2024, 719–729; first four authors confirmed |
| levy2024same | Crossref DOI 10.18653/v1/2024.acl-long.818 | ACL 2024, 15339–15353 |
| hsieh2024ruler | arXiv API 2404.06654 | title and first three authors confirmed |
| yoran2023robust | arXiv API 2310.01558 | title and first three authors confirmed |
| jin2024longcontext | arXiv API 2410.05983 | title and first three authors confirmed |
| parnas1972criteria | Crossref DOI 10.1145/361598.361623 | CACM 15(12), 1053–1058, 1972 |
| liskov1994behavioral | Crossref DOI 10.1145/197320.197383 | ACM TOPLAS 16(6), 1811–1841, 1994 |
| legunsen2016extensive | Crossref DOI 10.1145/2950290.2950361 | FSE 2016, 583–594; first four authors confirmed |
| gligoric2015practical | Crossref DOI 10.1145/2771783.2771784 | ISSTA 2015, 211–222 |
| jimenez2023swebench | arXiv API 2310.06770 | title and first four authors confirmed; venue (ICLR 2024) not asserted |
| ignatiev2019abduction | Crossref DOI 10.1609/aaai.v33i01.33011511 | AAAI 2019, vol. 33, 1511–1519 |
| darwiche2020reasons | arXiv API 2002.09284 | title and both authors confirmed; venue (ECAI 2020) not asserted |

Unverified references: none. Nothing is cited that is not in this table.
The MinCtx footnote from the first draft was removed.
