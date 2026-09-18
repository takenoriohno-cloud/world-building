# 知識系呪文 (Knowledge Spells)

本ドキュメントは、ガープス第4版『魔法大全』第15章（pp.92-97）および公式拡張サプリメント（『Magic: Artillery Spells』『Magic: Death Spells』『Magic: The Least of Spells』『Magic: Plant Spells』等）に準拠した、**全59種**の知識系呪文公式アーカイブです。マナ力学、生体媒介作用、ならびに2026年現代における結界都市防衛・軍事兵器工学・法規制（CR）の運用データを過不足なく完全網羅しています。

---

## 1. 知識系呪文の力学体系

知識系呪文は、マナの指向性周波数を介して対象の物理・生体・霊的パラメータを励起・変調・制御する魔術体系です。
- **生体媒介原則**: マナは術士の生体・神経系・霊体を介して作用し、直接の物質変換や物理エネルギー励起を行います。
- **現代技術インフラとの並行性**: 電子回路や通信網を直接破壊するのではなく、物理的現象（熱、圧力、電磁、物質変形等）を介して現代兵器や都市防護壁と相互作用します。

### 1.1 知識系呪文 前提条件ツリー (Prerequisite Tree)

```mermaid
graph TD
    %% クラススタイル定義（高コントラスト・ダークモード規格）
    classDef spell fill:#0f172a,stroke:#38bdf8,stroke-width:1.5px,color:#ffffff;
    classDef root fill:#0369a1,stroke:#38bdf8,stroke-width:2px,color:#ffffff,font-weight:bold;
    classDef ext fill:#1e293b,stroke:#94a3b8,stroke-width:1px,color:#cbd5e1,stroke-dasharray: 5 5;
    classDef special fill:#4c1d95,stroke:#c084fc,stroke-width:1.5px,color:#ffffff;

    %% 系統内呪文ノード定義
    subgraph Sub_3F1440AF ["52種"]
        Measurement["《測定》<br>(Measurement)"]:::root
        TellTime["《時計》<br>(Tell Time)"]:::root
        Alarm["《時報》<br>(Alarm)"]:::spell
        FarFeeling["《手触り》<br>(Far-Feeling)"]:::special
        FindDirection["《方位計》<br>(Find Direction)"]:::special
        TellPosition["《位置確認》<br>(Tell Position)"]:::spell
        TestLoad["《荷重調査》<br>(Test Load)"]:::spell
        SmallVision["《拡大視覚》<br>(Small Vision)"]:::spell
        EarthVision["《地中視覚》<br>(Earth Vision)"]:::spell
        AirVision["《霧中視覚》<br>(Air Vision)"]:::spell
        DetectMagic["《魔法感知》<br>(Detect Magic)"]:::special
        SenseMana["《マナ感知》<br>(Sense Mana)"]:::spell
        Aura["《霊気感知》<br>(Aura)"]:::spell
        Sp_14_5531["《呪文識別》<br>(（旧名：呪文感知）)"]:::spell
        Sp_15_2580["《魔術師眼》<br>(（旧名：魔力視覚）)"]:::spell
        Sp_16_4302["《魔術師覚》<br>(（旧名：魔力感知）)"]:::spell
        SeekMagic["《魔法探知》<br>(Seek Magic)"]:::spell
        AnalyzeMagic["《魔法分析》<br>(Analyze Magic)"]:::spell
        Sp_19_82C1["《時影召喚*》<br>(（旧名：影召喚）)"]:::spell
        GlassWall["《透明壁》<br>(Glass Wall)"]:::spell
        FarTasting["《遠隔毒見》<br>(Far-Tasting)"]:::special
        FarHearing["《遠耳》<br>(Far-Hearing)"]:::root
        WaterVision["《水中視覚》<br>(Water Vision)"]:::spell
        PlantVision["《木中視覚》<br>(Plant Vision)"]:::spell
        KnowLocation["《現在位置》<br>(Know Location)"]:::special
        KnowRecipe["《調合看破》<br>(Know Recipe)"]:::spell
        WizardEye["《魔法の目》<br>(Wizard Eye)"]:::spell
        InvisibleWizardEye["《透明な目》<br>(Invisible Wizard Eye)"]:::spell
        WizardMouth["《魔法の口》<br>(Wizard Mouth)"]:::spell
        WizardNose["《魔法の鼻》<br>(Wizard Nose)"]:::spell
        WizardHand["《魔法の手》<br>(Wizard Hand)"]:::spell
        Sp_32_50C0["《プラ視覚》<br>(（旧名：プラスチック視覚）)"]:::spell
        MetalVision["《金属視覚》<br>(Metal Vision)"]:::spell
        Sp_34_CED6["《星幽視覚*》<br>(（旧名：アストラル視覚）)"]:::spell
        Memorize["《記憶》<br>(Memorize)"]:::spell
        Pathfinder["《道案内》<br>(Pathfinder)"]:::special
        Projection["《幻視》<br>(Projection)"]:::spell
        Seeker["《方向探知》<br>(Seeker)"]:::special
        Trace["《追跡》<br>(Trace)"]:::spell
        Sp_40_14F8["《来歴》<br>(（旧名：歴史）)"]:::spell
        AncientHistory["《古代史》<br>(Ancient History)"]:::spell
        Prehistory["《前史》<br>(Prehistory)"]:::spell
        Sp_43_2E47["《呪文履歴》<br>(（旧名：呪文復元）)"]:::special
        KnowTrueShape["《本性感知》<br>(Know True Shape)"]:::special
        Recall["《回想》<br>(Recall)"]:::special
        RememberPath["《道順追憶》<br>(Remember Path)"]:::spell
        SeeSecrets["《隠匿看破》<br>(See Secrets)"]:::spell
        SchematicTL["《設計図/TL*》<br>(Schematic/TL)"]:::spell
        Sp_49_22C1["《残香再現》<br>(（旧名：過去嗅覚）)"]:::special
        Sp_50_F8D2["《残影再現》<br>(（旧名：過去視覚）)"]:::special
        Sp_51_B16C["《残響再現》<br>(（旧名：過去聴覚）)"]:::special
        DivinationAstrologyAuguryCartomancyCrystalGazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerologyorarithmancyOneiromancyPhysiognomyPyromancySortilegeSymbolCasting["《神託L-占星術L-前兆占いL-カード占いL-水晶占いL-こっくりさんL-腸占いL-霊感占いL-土占いL-波紋占いL-数字占いL-夢占いL-観相術L-火占いL-くじ占いL-紋章占い》<br>(DivinationAstrologyAuguryCartomancyCrystal-GazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerology, or arithmancyOneiromancyPhysiognomyPyromancySortilegeSymbol-Casting)"]:::spell
    end

    subgraph Sub_E032978 ["MAS / MDS 拡張 2種"]
        ForbiddenWisdom["《禁断の知恵*》<br>(Forbidden Wisdom)"]:::special
        VisionofDoom["《絶望視*》<br>(Vision of Doom)"]:::special
    end

    %% 前提条件依存関係エッジ
    TellTime --> Alarm
    Req_1 --> FarFeeling
    Req_1 --> FindDirection
    Measurement --> TellPosition
    Measurement --> TestLoad
    Ext_2 --> SmallVision
    Ext_3 --> EarthVision
    Ext_4 --> AirVision
    Req_1 --> DetectMagic
    DetectMagic --> SenseMana
    DetectMagic --> Aura
    DetectMagic --> Sp_14_5531
    DetectMagic --> Sp_15_2580
    DetectMagic --> Sp_16_4302
    DetectMagic --> SeekMagic
    Sp_14_5531 --> AnalyzeMagic
    Ext_5 --> Sp_19_82C1
    Ext_6 --> Sp_19_82C1
    EarthVision --> GlassWall
    Ext_7 --> FarTasting
    Ext_8 --> FarTasting
    Ext_9 --> WaterVision
    Ext_10 --> PlantVision
    TellPosition --> KnowLocation
    FarTasting --> KnowRecipe
    Ext_11 --> KnowRecipe
    Ext_12 --> WizardEye
    Ext_13 --> WizardEye
    WizardEye --> InvisibleWizardEye
    Ext_14 --> InvisibleWizardEye
    Ext_12 --> WizardMouth
    FarTasting --> WizardMouth
    Ext_15 --> WizardMouth
    Ext_12 --> WizardNose
    FarTasting --> WizardNose
    Ext_16 --> WizardHand
    FarFeeling --> WizardHand
    Ext_17 --> Sp_32_50C0
    Ext_18 --> MetalVision
    Ext_19 --> Sp_34_CED6
    Ext_20 --> Sp_34_CED6
    Ext_21 --> Memorize
    Req_22 --> Pathfinder
    Ext_19 --> Projection
    Req_22 --> Seeker
    Seeker --> Trace
    Trace --> Sp_40_14F8
    Sp_40_14F8 --> AncientHistory
    AncientHistory --> Prehistory
    Sp_40_14F8 --> Sp_43_2E47
    Sp_14_5531 --> Sp_43_2E47
    Aura --> KnowTrueShape
    Ext_23 --> KnowTrueShape
    Ext_23 --> Recall
    Ext_21 --> Recall
    FindDirection --> RememberPath
    Ext_23 --> RememberPath
    Seeker --> SeeSecrets
    Aura --> SeeSecrets
    Ext_24 --> SchematicTL
    Sp_40_14F8 --> SchematicTL
    Sp_40_14F8 --> Sp_49_22C1
    Ext_25 --> Sp_49_22C1
    Sp_40_14F8 --> Sp_50_F8D2
    Ext_26 --> Sp_50_F8D2
    Sp_40_14F8 --> Sp_51_B16C
    Ext_27 --> Sp_51_B16C
    Sp_40_14F8 --> DivinationAstrologyAuguryCartomancyCrystalGazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerologyorarithmancyOneiromancyPhysiognomyPyromancySortilegeSymbolCasting
    Ext_28 --> DivinationAstrologyAuguryCartomancyCrystalGazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerologyorarithmancyOneiromancyPhysiognomyPyromancySortilegeSymbolCasting
    Ext_29 --> DivinationAstrologyAuguryCartomancyCrystalGazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerologyorarithmancyOneiromancyPhysiognomyPyromancySortilegeSymbolCasting
    Ext_30 --> DivinationAstrologyAuguryCartomancyCrystalGazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerologyorarithmancyOneiromancyPhysiognomyPyromancySortilegeSymbolCasting
    Ext_31 --> DivinationAstrologyAuguryCartomancyCrystalGazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerologyorarithmancyOneiromancyPhysiognomyPyromancySortilegeSymbolCasting
    Ext_32 --> DivinationAstrologyAuguryCartomancyCrystalGazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerologyorarithmancyOneiromancyPhysiognomyPyromancySortilegeSymbolCasting
    EarthVision --> DivinationAstrologyAuguryCartomancyCrystalGazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerologyorarithmancyOneiromancyPhysiognomyPyromancySortilegeSymbolCasting
    WaterVision --> DivinationAstrologyAuguryCartomancyCrystalGazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerologyorarithmancyOneiromancyPhysiognomyPyromancySortilegeSymbolCasting
    Ext_33 --> DivinationAstrologyAuguryCartomancyCrystalGazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerologyorarithmancyOneiromancyPhysiognomyPyromancySortilegeSymbolCasting
    Ext_34 --> DivinationAstrologyAuguryCartomancyCrystalGazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerologyorarithmancyOneiromancyPhysiognomyPyromancySortilegeSymbolCasting
    Ext_35 --> DivinationAstrologyAuguryCartomancyCrystalGazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerologyorarithmancyOneiromancyPhysiognomyPyromancySortilegeSymbolCasting
    Ext_36 --> DivinationAstrologyAuguryCartomancyCrystalGazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerologyorarithmancyOneiromancyPhysiognomyPyromancySortilegeSymbolCasting
    Ext_37 --> DivinationAstrologyAuguryCartomancyCrystalGazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerologyorarithmancyOneiromancyPhysiognomyPyromancySortilegeSymbolCasting
    Ext_38 --> DivinationAstrologyAuguryCartomancyCrystalGazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerologyorarithmancyOneiromancyPhysiognomyPyromancySortilegeSymbolCasting
    Ext_39 --> DivinationAstrologyAuguryCartomancyCrystalGazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerologyorarithmancyOneiromancyPhysiognomyPyromancySortilegeSymbolCasting
    Ext_40 --> DivinationAstrologyAuguryCartomancyCrystalGazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerologyorarithmancyOneiromancyPhysiognomyPyromancySortilegeSymbolCasting
    Ext_41 --> DivinationAstrologyAuguryCartomancyCrystalGazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerologyorarithmancyOneiromancyPhysiognomyPyromancySortilegeSymbolCasting
    Ext_42 --> DivinationAstrologyAuguryCartomancyCrystalGazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerologyorarithmancyOneiromancyPhysiognomyPyromancySortilegeSymbolCasting
    Ext_43 --> DivinationAstrologyAuguryCartomancyCrystalGazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerologyorarithmancyOneiromancyPhysiognomyPyromancySortilegeSymbolCasting
    Recall --> ForbiddenWisdom
    SeeSecrets --> ForbiddenWisdom
    Ext_44 --> VisionofDoom

    %% 外部系統・特殊前提ノード
    Req_1["【前提: 素質1】"]:::ext
    Ext_2["【他系統: 《視覚鋭敏化》】"]:::ext
    Ext_3["【他系統: 《土変化》】"]:::ext
    Ext_4["【他系統: 《空気変化》】"]:::ext
    Ext_5["【他系統: 《霊魂召喚》】"]:::ext
    Ext_6["【他系統: 《神託》】"]:::ext
    Ext_7["【他系統: 《食料探知》】"]:::ext
    Ext_8["【他系統: 《空気探知》】"]:::ext
    Ext_9["【他系統: 《水変化》】"]:::ext
    Ext_10["【他系統: 《植物変化》】"]:::ext
    Ext_11["【他系統: 《味付け》】"]:::ext
    Ext_12["【他系統: 《念動》】"]:::ext
    Ext_13["【他系統: 《感覚鋭敏化/視覚》】"]:::ext
    Ext_14["【他系統: 《透明術》】"]:::ext
    Ext_15["【他系統: 《拡声》】"]:::ext
    Ext_16["【他系統: 《見えない手》】"]:::ext
    Ext_17["【他系統: 《プラ変化》】"]:::ext
    Ext_18["【他系統: 《金属変化》】"]:::ext
    Ext_19["【他系統: 《霊魂感知》】"]:::ext
    Ext_20["【他系統: 《透明看破》】"]:::ext
    Ext_21["【他系統: 《知恵》】"]:::ext
    Req_22["【前提: 素質1、知力12以上、探知系呪文2種】"]:::ext
    Ext_23["【他系統: 《幻覚感知》】"]:::ext
    Ext_24["【他系統: 《機能看破》】"]:::ext
    Ext_25["【他系統: 《芳香》】"]:::ext
    Ext_26["【他系統: 《単純幻覚》】"]:::ext
    Ext_27["【他系統: 《発声》】"]:::ext
    Ext_28["【他系統: 《占星術》】"]:::ext
    Ext_29["【他系統: 《気象予測》】"]:::ext
    Ext_30["【他系統: 《前兆占い》】"]:::ext
    Ext_31["【他系統: 《カード占い》】"]:::ext
    Ext_32["【他系統: 《水晶占い》】"]:::ext
    Ext_33["【他系統: 《こっくりさん》】"]:::ext
    Ext_34["【他系統: 《腸占い》】"]:::ext
    Ext_35["【他系統: 《霊感占い》】"]:::ext
    Ext_36["【他系統: 《土占い》】"]:::ext
    Ext_37["【他系統: 《波紋占い》】"]:::ext
    Ext_38["【他系統: 《数字占い》】"]:::ext
    Ext_39["【他系統: 《夢占い》】"]:::ext
    Ext_40["【他系統: 《観相術》】"]:::ext
    Ext_41["【他系統: 《火占い》】"]:::ext
    Ext_42["【他系統: 《くじ占い》】"]:::ext
    Ext_43["【他系統: 《紋章占い》】"]:::ext
    Ext_44["【他系統: 《時影召喚》】"]:::ext
```


---

## 2. ガープス第4版『魔法大全』基本知識系呪文（52種）

| 呪文名（日 / 英） | クラス | 持続時間 | 基本消費 / 維持 | 詠唱時間 | 前提条件 | 効果概要・力学 |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **《測定》**<br>Measurement | 範囲/情報 | 一瞬 | 1 | 1秒 | - | 目標 について、次の事柄のうち1つを知ることができます。 重量 正確な寸法 その場所 体積。 この 呪文 による情報は、 術者 にとって自然な方式で与えられます。測定は、 術者 が理解できる範囲で正確です。 一般に測定される量が異なっているような世界設定では、測定されるものも違ってきます。たとえば 文明レベ |
| **《時計》**<br>Tell Time | 情報 | 一瞬 | 1 | 1秒 | - | 術者 はいま何時かわかります。およその年月日もわかります。 |
| **《時報》**<br>Alarm | 通常 | 1週間 | 1 | 1秒 | 《時計》 | 未来のある特定の時間になったら、 目標 にそのことを知らせます。必要があれば目を覚まさせます。 術者 がをかけるときに知っていることであれば（それをメッセージにするなどして） 目標 にある事柄を思い出させることもできるでしょう。 呪文 をかける時点から1週間以内の日時を指定してください。 |
| **《手触り》**<br>Far-Feeling | 通常 | 1分 | 3/1 | 3秒 | 素質1 | 術者 は視界内の 目標 （どれだけ遠くても構いません）を実際に触ったかのように感じることができます。または厚さ1.8メートル未満の障害物を通してものを「触る」ことができます。 触覚判定 ? （手触り、温度、固さ、重さなど 触覚 ? は 聴覚 や 視覚 と同様に 知力 を基準に判定します）には自動的に成功します。この 触覚 ? は一方通行です。相手に |
| **《方位計》**<br>Find Direction | 情報 | 一瞬 | 2 | 1秒 | 素質1 | 術者 にはどちらが北かがわかります。「自分の家がどちらにあるのか」を知ることもできます（ただし1回の 呪文 で両方わかるわけではありません）。「本当の家」は1つしか設定できません。放浪者にはこうした「家」はないでしょう。 |
| **《位置確認》**<br>Tell Position | 情報 | 一瞬 | 1 | 1秒 | 《測定》 | 術者 は 目標 の正確な距離、方位、高度（ 術者 との相対的な）を知ることができます。 術者 と 目標 の間に視線を遮るものがあってはいけません。 |
| **《荷重調査》**<br>Test Load | 範囲/情報 | 一瞬 | 2# | 1秒 | 《測定》 | 術者 は 目標 にどれだけの力が加わると曲がったり壊れたりするかを知ることができます。これは橋、かご、ロープなどの能力を明らかにします。 |
| **《拡大視覚》**<br>Small Vision | 通常 | 1分 | 4/2# | 2秒 | 《視覚鋭敏化》ないし光・闇系5種、「視覚障害」「視力が悪い」なし | 有利特徴「拡大視覚」 B42P |
| **《地中視覚》**<br>Earth Vision | 通常 | 30秒 | 2/10ｍ毎# | 1秒 | 《土変化》 | 土を見通し、洞窟、鉱脈、埋められた宝物、埋葬された死体などを見つけることができます。見通せるのは、土や加工されていない石（厚さ50メートルまで）だけです。金属、加工された石、レンガなどは見通せません。つまり、城壁を見通すことはできません。 |
| **《霧中視覚》**<br>Air Vision | 通常 | 1秒 | 1/1.5km毎/半 | 1秒 | 《空気変化》 | 煙 、 霧 、埃、 砂嵐 の中でもはっきりとものが見えます。空気の状態による 視覚 の修正が無効化されます。 |
| **《魔法感知》**<br>Detect Magic | 通常 | 一瞬 | 2 | 5秒 | 素質1 | 目標 の物体が、 魔法の品物 かどうかわかります。2回成功すれば、 呪文 が一時的なものか、 永久 にかかっているかどうかもわかります。どちらかに クリティカル で成功すれば、を使ったときのように、どんな 呪文 かまで完全にわかります。 これは「 魔法の素質 0レベル」に付随する、 魔法の品物 を感知する能力とは異なります。 素質 |
| **《マナ感知》**<br>Sense Mana | 情報 | 一瞬 | 3 | 5秒 | 《魔法感知》 | ルール 呪文データ 呪文 Fantasy |
| **《霊気感知》**<br>Aura | 情報 | 一瞬 | 3 | 1秒 | 《魔法感知》 | 霊・目標 のまわりに輝くオーラ、つまり「霊気」を感知します。 術者 は霊気によって、 目標 の個性を見通すことができます。 技能 判定の 成功度 が高いほど、より詳しく知ることができます。とくに 目標 が「 魔法の素質 」「 魔法の耐性 」「 魔法の影響を受けやすい 」 特徴 （およびそのレベル）を持っているかどうか、 目標 が何かの手段で 憑 |
| **《呪文識別》**<br>（旧名：呪文感知）<br>Identify Spell | 情報 | 一瞬 | 2 | 1秒 | 《魔法感知》 | ルール 呪文データ 呪文 差替名称 |
| **《魔術師眼》**<br>（旧名：魔力視覚）<br>Mage Sight | 通常 | 1分 | 3/2 | 1秒 | 《魔法感知》 | 年09月21日(木) 17:23:52 履歴 |
| **《魔術師覚》**<br>（旧名：魔力感知）<br>Mage Sense | 情報 | 1分 | 3/2 | 1秒 | 《魔法感知》 | 呪文データ 差替名称 差替名称 呪文 |
| **《魔法探知》**<br>Seek Magic | 情報 | 一瞬 | 6 | 10秒 | 《魔法感知》 | もっとも近い位置にある、ある程度以上の魔力を持った品物・効果を発揮している 呪文 ・ 魔法 的な生物（悪魔、精霊、霊魂など。ただし「 魔法の素質 」をもつ個人はこれに含まれません）の方向とおよその距離が分かります。通常の 距離修正 値を使います。 術者 はすでに知っている 魔法 をあらかじめ省いたうえで 呪文 を欠けるこ |
| **《魔法分析》**<br>Analyze Magic | 情報/抵-呪文 | 一瞬 | 8 | 1時間 | 《呪文識別》 | __調査を妨害する 呪文 、 目標 にかかっている 呪文 が正確に分かります。複数の 呪文 がかかっている場合、 |
| **《時影召喚*》**<br>（旧名：影召喚）<br>Summon Shade* | 情報/抵-意志力 | 1分 | 50/20 | 10分 | 《霊魂召喚》ないし《神託》 | 召喚・呪文データ まだ |
| **《透明壁》**<br>Glass Wall | 通常 | 1分 | 4/2 | 1秒 | 知識系5種ないし《地中視覚》 | 厚さ1.2メートルまでの壁、床、天井などの障壁を通してものを見ることができます（物質が何であるかは関係ありません）。 |
| **《遠隔毒見》**<br>Far-Tasting | 通常 | 1分 | 3/1 | 3秒 | 素質1、《食料探知》ないし《空気探知》、「嗅覚・味覚消失」ではない | 目標 は視界内（どれほど遠くても構いません）にある物の味と匂いを感じ取ることができます。あるいは、厚さの合計が2メートル未満の固体を通して味や匂いを感じ取ります。 目標 は 味覚/嗅覚判定 には自動的に成功します。しかし、通常では味や臭いを感じとれない物質（たとえば一酸化炭素のような無味無臭の気体）は感知できません。 毒 の効果は臭いでは |
| **《遠耳》**<br>Far-Hearing | 情報 | 1分 | 4/2 | 3秒 | 素質1、音声系4種、「聴覚障害」「難聴」なし | 術者 は視界内で行われている会話を何でも聞き取れます。どんなに離れていてもよく、厚さの合計が1.8メートル以内の固体があいだにあってもかまいません。 術者 はあらゆる 聴覚判定 に自動的に成功します。 |
| **《水中視覚》**<br>Water Vision | 情報 | 30秒 | 1/1# | 1秒 | 《水変化》 | 水や雪、氷のなかでも視界が利き、沈んだ財宝や徘徊する怪物を発見できます。 |
| **《木中視覚》**<br>Plant Vision | 通常 | 30秒 | 1/10ｍ毎 | 1秒 | 《植物変化》 | 植物を見通して、植物に覆われた建物や徘徊する敵などを発見できます。自然の植物の茂みはすべて透けて見えます。ただし、 魔法 の木立ちや枯れた森や木造建築物などは見通せません。 |
| **《現在位置》**<br>Know Location | 情報 | 一瞬 | 2 | 10秒 | 素質1、《位置確認》 | 術者 は現在いる地名（その周辺2〜3キロが何と呼ばれているか）を知ることができます。これは 術者 が知っている有名な場所によって表現されます（ 術者 がその地名を知っているかどうか怪しいときには、（〈 地域知識 〉判定を行います）。 例：「今はサハラ砂漠にいる。ティンブクトゥの北、約45キロの地点」 |
| **《調合看破》**<br>Know Recipe | 情報/抵-特殊 | 1日 # | 3 | 15秒 | 《遠隔毒見》、《味付け》 | _特殊、 食べ物1点に唱えると、その材料と調理方法のすべてが 術者 の心の中に浮かびます。 この 呪文 は、 錬金術 で作られたものにも使えます。しかし、そうした 霊薬 （エリクサ）は作成した 錬金術 師の 技能レベル で 呪文 に抵抗します。 GM の裁量によって、薬物類にこの 呪文 が使えるようにしても構いません。これは |
| **《魔法の目》**<br>Wizard Eye | 通常 | 1分 | 4/2 | 2秒 | 《念動》、《感覚鋭敏化/視覚》 | 5センチの球形をした目を作り出し、 術者 はその目を通してものを見ることができます。目は空中を垂直にも水平にも飛びます。 移動力 は10です――つまり、 術者 の ターン 1秒に10メートル 移動 します。 移動 させるには 集中 が必要ですが、見るだけなら 集中 しなくてもかまいません。 視覚 に影響をあたえる 魔法 がこのほかにも 術者 にかかっている場 |
| **《透明な目》**<br>Invisible Wizard Eye | 通常 | 1分 | 5/3 | 4秒 | 《魔法の目》、《透明術》 | でしか見ることができないを作り出します。そこに目がありそうだと推測できるなら、 攻撃 をしかけることもできますが、 サイズ修正 で-7、見えないことにより-6の修正があるので、命中させるのは至難の技です。 |
| **《魔法の口》**<br>Wizard Mouth | 通常 | 1分 | 4/2 | 2秒 | 《念動》、《遠隔毒見》、《拡声》 | 術者 によく似た10センチほどの口と唇を作り出します。 術者 はその口を通じて喋ったり味わうことができます。口は 移動力 10で 術者 の ターン に 移動 しますが、ものにぶつかりそうであれば 移動 しないかもしれませんと組み合わせない限り）。 移動 させるには 集中 が必要ですが、喋 |
| **《魔法の鼻》**<br>Wizard Nose | 通常 | 1分 | 3/2 | 2秒 | 《念動》、《遠隔毒見》 | 術者 によく似た5〜8センチほどの鼻を作り出します。 術者 はその鼻を通じて匂いをかぐことができます。鼻は 移動力 10で 術者 の ターン に 移動 しますが、ものにぶつかりそうであれば 移動 しないかもしれません（と組み合わせない限り）。 移動 させるには 集中 が必要ですが、匂いをかぐだけなら 集中 |
| **《魔法の手》**<br>Wizard Hand | 通常 | 1分 | さまざま | 3秒 | 《見えない手》、《手触り》 | 呪文データ 呪文データ 移動・衝突・踏み・落下 |
| **《プラ視覚》**<br>（旧名：プラスチック視覚）<br>Plastic Vision | 通常 | 30秒 | 2/5ｍ毎/同 | 1秒 | 《プラ変化》 | 呪文 （ 金属・）、 プラスチック を見通します。 |
| **《金属視覚》**<br>Metal Vision | 通常 | 30秒 | 2/5ｍ毎/同 | 1秒 | 《金属変化》 | （ 金属・）、 金属 を通して、その奥にあるものを見ます。扉の向こうや箱の中などが見られます。特定の 金属 （鉛）はこの 呪文 に完全に抵抗するか、阻みます。 |
| **《星幽視覚*》**<br>（旧名：アストラル視覚）<br>Astral Vision* | 通常 | 1分 | 4/2 | 1秒 | 《霊魂感知》、《透明看破》 | 呪文データ 呪文データ 霊・ |
| **《記憶》**<br>Memorize | 通常 | 1日 # | 3 | 2秒 | 《知恵》ないし知識系6種 | 霊薬 『 記憶薬 』の旧名。 |
| **《道案内》**<br>Pathfinder | 情報 | 一瞬 | 4 | 10秒 | 素質1、知力12以上、探知系呪文2種 | ある場所の方向か、そこへたどり着く適当な道筋がわかります――どちらを知りたいか、選んでください。 長距離の修正値 を使います。 術者 がその場所へ行ったことがないときは、 GM が不利な修正を与えてください。その場所が実在するかどうか、 術者 が確信をもてないときにはかなり大きな修正がかかります。この 呪文 で人間や物体を見つけることはできません |
| **《幻視》**<br>Projection | 通常 | 1分 | 4/2 | 3秒 | 《霊魂感知》、知識系4種 | 霊・術者 の精神は一時的に肉体を抜け出します。視界内にある任意の一点（ 長距離の修正値 を用います）へと移動します。霊体は実体を持ちませんが、五感は働きます。その存在はやなどによって認識することができます。他の方法では認識されません。 霊体はの効果範囲を |
| **《方向探知》**<br>Seeker | 情報 | 一瞬 | 3 | 1秒 | 素質1、知力12以上、探知系呪文2種 | 特定の人物や人工の品物を探すことができます。 技能 判定に成功すれば、品物のある場所の情景が浮かぶか、1.5キロメートル以内ならじっさいにその場所に導いてくれます。 人を捜すためには、 術者 はその名前を知っているか、顔を思い浮かべることができなければなりません。例えば 目標 をよく知らないのに殺人事件を解決するために “ 殺人犯を捜す ” と |
| **《追跡》**<br>Trace | 通常 | 1時間 | 3/1 | 1分 | 《方向探知》 | 物体や生き物にかけると、 呪文 が 維持 されているかぎり、1秒 集中 すれば、 目標 がどこにあるかがわかります。あらかじめ一緒にいるときにをかけておくか、あるいはで位置を確認してかけます。 目標 が遠い場合、 長距離の修正値 を使います。 |
| **《来歴》**<br>（旧名：歴史）<br>History | 情報 | 一瞬 | さまざま | 秒=コスト | 《追跡》 | ルール 呪文データ 差替名称 |
| **《古代史》**<br>Ancient History | 情報 | 一瞬 | さまざま | 分=コスト | 《来歴》 | に似ていますが、品物のより長い時間の一般的な印象がわかります。 |
| **《前史》**<br>Prehistory | 情報 | 一瞬 | さまざま | 時間=コスト | 《古代史》 | と同様ですが、千年単位のあまり特定的でない情報がわかります。品物の年代や機能は常にわかりますが、何か重大事に関わった品でないかぎり、年代と機能以外のことはわかりません。幸いなことに、を最も頻繁に使う考古学者にとってはそれで充分なのです。 |
| **《呪文履歴》**<br>（旧名：呪文復元）<br>Reconstruct Spell | 情報 | 一瞬 | 3# | 10秒 | 素質2、《来歴》、《呪文識別》 | ルール 呪文データ 差替名称 |
| **《本性感知》**<br>Know True Shape | 情報 | 一瞬 | 2 | 1秒 | 素質1、特定変身系呪文1種、 《霊気感知》ないし《幻覚感知》 | 術者 はの 呪文 や類似の 魔法 的効果――や 幻覚 の類を含みます――を受けている 目標 の本体を知ることができます。 術者 は 目標 を視認できる状況でなければなりません。この 呪文 では、正体についての一般的な事柄もわかります。 クリティカル で成功すると、本体の性質（一般的に知られている名前と外見）と偽装に |
| **《回想》**<br>Recall | 通常 | 1日 # | 4 | 10秒 | 素質2、《幻覚感知》、《知恵》 | 目標 は忘れていたりあやふやな事実や出来事を思い起こします。「 写真記憶 」の 特徴 （『 ベーシックセット 1巻』58ページ）を持っているかのように扱います。思い出そうとする出来事までの時間に応じて、 時間修正表 （135ページ）を適用します。「 記憶力 」の 特徴 があれば+5、「 写真記憶 」があれば+10の修正があります（「 写真 |
| **《道順追憶》**<br>Remember Path | 通常 | 1時間 | 3/1 | 10秒 | 《方位計》、《幻覚感知》 | 詳細参照 |
| **《隠匿看破》**<br>See Secrets | 通常 | 1分 | 5/2 | 5秒 | 《方向探知》、《霊気感知》 | 隠された品物、扉、罠などが、はっきり目に見えるようになります。故意に隠したものでないと 呪文 は効きません――つまり、失くしたものは見つかりません。 |
| **《設計図/TL*》**<br>Schematic/TL* | 情報 | 1分 | 5/半# | 5秒 | 《機能看破》、《来歴》 | （至難） pp.40-41 （至難） 、 術者 の脳内に、 目標 の 機械 の詳細で専門的な “青写真” を作りだします。 術者 は紙の 設計図 を調べるのと同じ時間で、自分の脳内の 設計図 を読むことができます。ただし、この 呪文 によって、読 |
| **《残香再現》**<br>（旧名：過去嗅覚）<br>Scents of the Past | 通常 | 1分 | 1/1# | 10秒 | 素質2、《来歴》、《芳香》 | 。 呪文 壁などの物体に対して唱えます。この 呪文 は 目標 が過去に “ かいだ ” （過去に触れた・染み付いた）匂いを再現します。 術者 は唱えるさいに再生を開始する時間を指定します。 時間修正表 を用います（135ページ）。1つの 目標 |
| **《残影再現》**<br>（旧名：過去視覚）<br>Images of the Past | 通常 | 1分 | 3/3# | 10秒 | 素質2、《来歴》、《単純幻覚》 | 。 呪文 光・鏡など反射する面に対して唱えます。この 呪文 はその面が過去に「見た」場面を「再生」します。 術者 は唱えるさいに再生を開始する時間を指定します（「今から1年前にこの部屋で何があったか映しなさい......」）。 時間修正表 を用 |
| **《残響再現》**<br>（旧名：過去聴覚）<br>Echoes of the Past | 通常 | 1分 | 2/2# | 10秒 | 素質2、《来歴》、《発声》 | 。 呪文 壁、床などの物体に対して唱えます。この 呪文 は 目標 が過去に「聞いた」音声を「再生」します。 術者 は唱えるさいに再生を開始する時間を指定します（「今から1年前にこの部屋で何が話されたか教えなさい.......」）。 時 |
| **《神託L-占星術L-前兆占いL-カード占いL-水晶占いL-こっくりさんL-腸占いL-霊感占いL-土占いL-波紋占いL-数字占いL-夢占いL-観相術L-火占いL-くじ占いL-紋章占い》**<br>DivinationAstrologyAuguryCartomancyCrystal-GazingDactylomancyExtispicyGastromancyGeomancyLecanomancyNumerology, or arithmancyOneiromancyPhysiognomyPyromancySortilegeSymbol-Casting | 情報 | 一瞬 | 10 | 1時間# | 《来歴》、他の呪文#《占星術》は《来歴》、《気象予測》、〈天文学/Lv15以上〉技能。《前兆占い》は《来歴》、四大精霊系呪文から1種ずつ。《カード占い》は《来歴》、四大精霊系呪文から1種ずつ。《水晶占い》は《来歴》、《地中視覚》あるいは《水中視覚》。《こっくりさん》は《来歴》、四大精霊系呪文から1種ずつ。《腸占い》は《来歴》、動物系呪文4種。《霊感占い》は《来歴》、〈催眠術/Lv15以上〉技能あるいは精神操作系呪文を3種。《土占い》は《来歴》、地霊系呪文4種。《波紋占い》は《来歴》、水霊系呪文4種。《数字占い》は《来歴》、「数学能力」。《夢占い》は《来歴》、情報伝達系呪文4種。《観相術》は《来歴》、肉体操作系呪文4種。《火占い》は《来歴》、火霊系呪文4種。《くじ占い》は《来歴》、四大精霊系呪文から1種ずつ。《紋章占い》は《来歴》、〈紋章学/Lv15以上〉技能。 | ルール 呪文データ まだ |

---

## 3. 魔導兵器・砲兵戦術拡張呪文（MAS / MDS 拡張 2種）

| 呪文名（日 / 英） | クラス | 持続時間 | 基本消費 / 維持 | 詠唱時間 | 前提条件 | 効果概要・力学 |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **《禁断の知恵*》**<br>Forbidden Wisdom * | 通常/抵-知力 | 一瞬 | 11 | 5秒 | 素質3、《回想》、《隠匿看破》 | （至難）（Forbidden Wisdom (VH)） p.15 （至難） _ 知力 運命、神、または「 知る能わざるもの 」によって、生きている定命の存在に禁じられた真実を明らかにします。 知力 0〜5の対象には効果ありません（ 知性 を持たぬことがこの 呪文 への免疫となります）。 知力 6以上のター |
| **《絶望視*》**<br>Vision of Doom * | 通常/抵-知力 | 特殊 | 10 | 3秒 | 素質3、《時影召喚》 | magic＿death＿spells |

---

## 4. 魔導兵器・砲兵戦術拡張呪文（MAS / MDS 拡張 5種）

| 呪文名（日 / 英） | クラス | 持続時間 | 基本消費 / 維持 | 詠唱時間 | 前提条件 | 効果概要・力学 |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **《病毒検査/種別》（並）**<br>（Test (A)） | 防御 | 一瞬 | 1 | 30秒 | -（簡単呪文なので） | （並）（Test (A)） p.10 （並） 特定の 病気 や 毒物 が被験者に影響を与えているかどうかを明らかにします。 それぞれの症状に対して異なる呪文が存在します…… （Test (Leprosy)）、 《 病毒検査 /蛇の毒 |
| **《置き場所回想》（並）**<br>（Keyfinder (A)） | 通常 | 一瞬 | 1 | 5秒 | -（簡単呪文なので） | （並）（Keyfinder (A)） p.11 （並） 術者 は、自分が所有しているが見つけられないアイテムをどこに置いたかを思い出します (事実や出来事などは決して思い出せません) 。これに対し、 GM は「（そのようなものを思い出すための）従来の 知力 判定へのボーナス」も提供します。通常は |
| **《真面目な話》（並）**<br>（Know Thyself (A)） | 通常 | 1分 | 2・1 | 5秒 | -（簡単呪文なので） | （並）（Know Thyself (A)） p.11 （並） 対象の考えを整理し、知識を正直に提示することのみを目的として、〈 演説 〉や〈 指導 〉に +1ボーナスを与えます。聞き手は、対象が嘘をついていないことを確認するための、〈 嘘発見 〉や〈 尋問 〉に +1ボーナスを得ます。この 呪文 は専 |
| **《甘い忘却》（並）**<br>（Sweet Oblivion (A)） | 通常 | 永久 | 3 | 10秒 | -（簡単呪文なので） | （並）（Sweet Oblivion (A)） p.11 （並） 術者 (だけ！) が 1つの事実 (言語、技能、呪文などではないもの) を永久に忘れます。恐ろしい何かを見たり学んだりしないようにしたり、読心を阻止したりするのに役立ちます。ただし本格的な魔法の尋問者を止めるには弱すぎま |
| **《魔法学師》（並）**<br>（Thaumatomancy (A)） | 情報 | 一瞬 | 10 | 1時間 | -（簡単呪文なので） | （並）（Thaumatomancy (A)） p.12 （並） はっきりと 魔法 に説明を求めてください。1回の詠唱で、既存の 魔法 について、〈 魔法学 〉 技能 が答えられる1つの質問に回答します。新しい 魔法 の独自の研究には使用できません。 技能 判定に影響するペナルティはこの 呪文 にも適用され |

---

## 5. 2026年現代戦術・都市防衛・法規制（CR）における運用

### 5.1 警察・自衛隊・PMCにおける実戦配備
結界都市（セーフゾーン）警備および壁外アウトランドへの遠征作戦において、知識系呪文は索敵・突入支援・防壁維持・目標無力化の標準プロトコルとして統合運用されています。特に部隊随伴術士による即時展開は、通常兵器との複合火力（コンバインド・アームズ）として極めて高い戦闘効率を発揮します。

### 5.2 メガコーポ支配と特許利権
ヤマト重工、テイコク製薬、サエデル・シュティフトゥング、アレス等のメガコーポは、知識系呪文の工業・医療・防衛利用に関する独占特許を保有しており、民間術士に対するライセンス管理や魔導触媒・霊薬の市場流通を掌握しています。

### 5.3 国際魔導協定（IMA）および法規制（CR）
破壊力・精神汚染・非人道性の高い高位呪文は、国家公安委員会および国際魔導協定により**規制等級CR3〜CR4（要特別国家許可・戦時国際法規制）**に指定されており、無認可での行使・研究は厳罰に処されます。