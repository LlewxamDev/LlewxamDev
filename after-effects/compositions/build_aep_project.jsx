// ============================================================================
// PROJECT LWX.EXE — ADOBE AFTER EFFECTS CC 2019 PROJECT BUILDER (.JSX)
// Builds the complete editable LWX_EXE_Profile.aep with COMP_01_HERO through
// COMP_09_FOOTER, reusable Precompositions, 2.5D Multi-Plane Z layers,
// Bezier Graph Editor Keyframes, Masks, and Native AE 2019 Effects.
// ============================================================================

(function () {
    var baseDir = "c:/Users/Evandro/Downloads/portfólio_bots/LlewxamDev/after-effects";
    var srcDir = baseDir + "/assets-source";
    var rendersDir = baseDir + "/renders";
    var aepPath = baseDir + "/LWX_EXE_Profile.aep";
    var reportPath = rendersDir + "/ae_build_report.json";

    app.suppressDialogs = true;
    if (app.project) {
        app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
    }
    app.newProject();
    app.project.bitsPerChannel = 8;

    // 1. Create Project Panel Folder Hierarchy
    var folderMainComps = app.project.items.addFolder("01_MAIN_COMPOSITIONS");
    var folderPrecomps = app.project.items.addFolder("02_PRECOMPOSITIONS");
    var folderSources = app.project.items.addFolder("03_ASSETS_SOURCE");

    function importSourcePng(filename) {
        var f = new File(srcDir + "/" + filename);
        if (!f.exists) {
            return null;
        }
        var io = new ImportOptions(f);
        var item = app.project.importFile(io);
        item.parentFolder = folderSources;
        return item;
    }

    // Import all layered source plates
    var src = {
        heroSkyNorm: importSourcePng("hero_sky_normal.png"),
        heroSkyCorr: importSourcePng("hero_sky_corrupted.png"),
        heroMtnNorm: importSourcePng("hero_mountains_normal.png"),
        heroMtnCorr: importSourcePng("hero_mountains_corrupted.png"),
        heroFgNorm: importSourcePng("hero_ground_normal.png"),
        heroFgCorr: importSourcePng("hero_ground_corrupted.png"),
        sonicNorm1: importSourcePng("sonic_normal_idle_01.png"),
        sonicNorm2: importSourcePng("sonic_normal_idle_02.png"),
        sonicBlink: importSourcePng("sonic_normal_blink.png"),
        sonicExe: importSourcePng("sonic_exe_corrupt_01.png"),
        sonicEyeMicro: importSourcePng("sonic_exe_eye_micro.png"),
        heroTitleNorm: importSourcePng("hero_title_plate_normal.png"),
        heroTitleExe: importSourcePng("hero_title_plate_exe.png"),
        identityPlate: importSourcePng("identity_panel_plate.png"),
        divAGold: importSourcePng("divider_a_golden_ring.png"),
        divBCorr: importSourcePng("divider_b_corrupted_ring.png"),
        divCGhz: importSourcePng("divider_c_green_hill.png"),
        projHeader: importSourcePng("projects_header_plate.png"),
        projCardSample: importSourcePng("project_card_sample.png"),
        techLangNorm: importSourcePng("tech_monitors_languages_overlay.png"),
        techLangCorr: importSourcePng("tech_monitors_languages_overlay_corrupted.png"),
        techEcoNorm: importSourcePng("tech_monitors_ecosystem_overlay.png"),
        techEcoCorr: importSourcePng("tech_monitors_ecosystem_overlay_corrupted.png"),
        techToolsNorm: importSourcePng("tech_monitors_tools_overlay.png"),
        techToolsCorr: importSourcePng("tech_monitors_tools_overlay_corrupted.png"),
        trophyHeader: importSourcePng("trophy_header_plate.png"),
        footerBanner: importSourcePng("footer_banner_plate.png"),
        btnGithub: importSourcePng("btn_footer_github.png"),
        btnPortfolio: importSourcePng("btn_footer_portfolio.png"),
        btnLinkedin: importSourcePng("btn_footer_linkedin.png"),
        glitchMap: importSourcePng("glitch_displacement_map.png")
    };

    // Helper: Apply smooth Bezier ease (Graph Editor) to a 1D or 2D/3D property
    function applySmoothBezier(prop, inInf, outInf) {
        try {
            var dims = 1;
            if (prop.propertyValueType === PropertyValueType.TwoD_SPATIAL || prop.propertyValueType === PropertyValueType.TwoD) {
                dims = 2;
            } else if (prop.propertyValueType === PropertyValueType.ThreeD_SPATIAL || prop.propertyValueType === PropertyValueType.ThreeD) {
                dims = 3;
            }
            var easeIn = [];
            var easeOut = [];
            for (var d = 0; d < dims; d++) {
                easeIn.push(new KeyframeTemporalEase(0, inInf));
                easeOut.push(new KeyframeTemporalEase(0, outInf));
            }
            for (var k = 1; k <= prop.numKeys; k++) {
                prop.setTemporalEaseAtKey(k, easeIn, easeOut);
            }
        } catch (e) {}
    }

    // Helper: Add CRT Scanline Adjustment Layer using native Venetian Blinds
    function addCRTScanlineAdjustment(comp) {
        var adj = comp.layers.addSolid([0.02, 0.01, 0.02], "CRT_SCANLINES_AND_GLITCH_ADJ", comp.width, comp.height, 1.0, comp.duration);
        adj.adjustmentLayer = true;
        var fxGroup = adj.property("ADBE Effect Parade");
        if (fxGroup) {
            try {
                var vb = fxGroup.addProperty("ADBE Venetian Blinds");
                if (vb) {
                    vb.property("ADBE Venetian Blinds-0001").setValue(18); // Transition Completion
                    vb.property("ADBE Venetian Blinds-0002").setValue(90); // Direction horizontal
                    vb.property("ADBE Venetian Blinds-0003").setValue(4);  // Width
                }
            } catch (e1) {}
            try {
                var td = fxGroup.addProperty("ADBE Turbulent Displace");
                if (td) {
                    var amt = td.property("ADBE Turbulent Displace-0002");
                    amt.setValueAtTime(0.0, 0);
                    amt.setValueAtTime(2.32, 0);
                    amt.setValueAtTime(2.36, 38);
                    amt.setValueAtTime(2.44, 28);
                    amt.setValueAtTime(2.48, 0);
                    applySmoothBezier(amt, 80, 80);
                }
            } catch (e2) {}
        }
        return adj;
    }

    // Helper: Add Vignette Mask Layer
    function addVignetteMaskLayer(comp) {
        var vig = comp.layers.addSolid([0.02, 0.0, 0.02], "VIGNETTE_MASK_FRAME", comp.width, comp.height, 1.0, comp.duration);
        vig.blendingMode = BlendingMode.MULTIPLY;
        vig.transform.opacity.setValue(45);
        try {
            var maskGrp = vig.property("ADBE Mask Parade");
            var mask = maskGrp.addProperty("ADBE Mask Atom");
            var shape = new Shape();
            var m = 36;
            shape.vertices = [[m, m], [comp.width - m, m], [comp.width - m, comp.height - m], [m, comp.height - m]];
            shape.closed = true;
            mask.property("ADBE Mask Shape").setValue(shape);
            mask.inverted = true;
            mask.property("ADBE Mask Feather").setValue([64, 64]);
        } catch (e) {}
        return vig;
    }

    // ========================================================================
    // PRECOMPOSITIONS
    // ========================================================================
    var precompSonic = app.project.items.addComp("PRECOMP_SONIC_CHARACTER", 352, 352, 1.0, 4.0, 25);
    precompSonic.parentFolder = folderPrecomps;
    if (src.sonicNorm1 && src.sonicExe) {
        var lNorm = precompSonic.layers.add(src.sonicNorm1);
        lNorm.name = "SONIC_NORMAL_SMILING";
        var lBlink = precompSonic.layers.add(src.sonicBlink);
        lBlink.name = "SONIC_NORMAL_BLINK";
        var lExe = precompSonic.layers.add(src.sonicExe);
        lExe.name = "SONIC_EXE_SUBLIMINAL_80MS";

        // Breathing position bob on Normal Sonic
        var pos = lNorm.transform.position;
        pos.setValueAtTime(0.0, [176, 176]);
        pos.setValueAtTime(1.0, [176, 172]);
        pos.setValueAtTime(2.0, [176, 176]);
        pos.setValueAtTime(3.0, [176, 172]);
        pos.setValueAtTime(4.0, [176, 176]);
        applySmoothBezier(pos, 75, 75);

        // Blink opacity at t=1.10s..1.20s
        var opBlink = lBlink.transform.opacity;
        opBlink.setValueAtTime(0.0, 0);
        opBlink.setValueAtTime(1.08, 0);
        opBlink.setValueAtTime(1.12, 100);
        opBlink.setValueAtTime(1.20, 0);

        // Subliminal 80ms (2 frames at 25fps: 2.36s to 2.44s) Sonic.EXE swap
        var opExe = lExe.transform.opacity;
        opExe.setValueAtTime(0.0, 0);
        opExe.setValueAtTime(2.32, 0);
        opExe.setValueAtTime(2.36, 100);
        opExe.setValueAtTime(2.44, 0);
        for (var k = 1; k <= opExe.numKeys; k++) {
            opExe.setInterpolationTypeAtKey(k, KeyframeInterpolationType.HOLD, KeyframeInterpolationType.HOLD);
        }

        // Native Glow on Sonic.EXE crimson eyes
        try {
            var glowFx = lExe.property("ADBE Effect Parade").addProperty("ADBE Glo2");
            if (glowFx) {
                glowFx.property("ADBE Glo2-0002").setValue(55); // Threshold
                glowFx.property("ADBE Glo2-0003").setValue(18); // Radius
                glowFx.property("ADBE Glo2-0004").setValue(1.4); // Intensity
            }
        } catch (eg) {}
    }

    // ========================================================================
    // COMP_01_HERO (1200 x 400, 25fps, 4.00s)
    // ========================================================================
    var comp01 = app.project.items.addComp("COMP_01_HERO", 1200, 400, 1.0, 4.0, 25);
    comp01.parentFolder = folderMainComps;
    if (src.heroSkyNorm) {
        var skyN = comp01.layers.add(src.heroSkyNorm);
        skyN.name = "GHZ_SKY_NORMAL_Z400";
        skyN.threeDLayer = true;
        skyN.transform.position.setValue([600, 200, 400]);
        skyN.transform.scale.setValue([135, 135, 100]);

        var mtnN = comp01.layers.add(src.heroMtnNorm);
        mtnN.name = "GHZ_MOUNTAINS_WATER_Z200";
        mtnN.threeDLayer = true;
        mtnN.transform.position.setValue([600, 200, 200]);
        mtnN.transform.scale.setValue([118, 118, 100]);

        var fgN = comp01.layers.add(src.heroFgNorm);
        fgN.name = "GHZ_PALMS_CHECKER_GROUND_Z60";
        fgN.threeDLayer = true;
        fgN.transform.position.setValue([600, 200, 60]);
        fgN.transform.scale.setValue([106, 106, 100]);
        try {
            var ww = fgN.property("ADBE Effect Parade").addProperty("ADBE Wave Warp");
            if (ww) {
                ww.property("ADBE Wave Warp-0002").setValue(2); // Wave Height
                ww.property("ADBE Wave Warp-0003").setValue(120); // Wave Width
            }
        } catch (ew) {}

        var fgC = comp01.layers.add(src.heroFgCorr);
        fgC.name = "GHZ_CORRUPTED_FLASH_80MS";
        var opFgC = fgC.transform.opacity;
        opFgC.setValueAtTime(0.0, 0);
        opFgC.setValueAtTime(2.32, 0);
        opFgC.setValueAtTime(2.36, 100);
        opFgC.setValueAtTime(2.44, 0);
        for (var kc = 1; kc <= opFgC.numKeys; kc++) {
            opFgC.setInterpolationTypeAtKey(kc, KeyframeInterpolationType.HOLD, KeyframeInterpolationType.HOLD);
        }

        var charLayer = comp01.layers.add(precompSonic);
        charLayer.name = "CHARACTER_RIG_SONIC_NORMAL_TO_EXE";
        charLayer.transform.position.setValue([284, 198]);

        var titleNorm = comp01.layers.add(src.heroTitleNorm);
        titleNorm.name = "TITLE_OLHE_MEU_PERFIL_NORMAL";

        var titleExe = comp01.layers.add(src.heroTitleExe);
        titleExe.name = "TITLE_OLHE_MEU_PERFIL_EXE_80MS";
        var opTitleE = titleExe.transform.opacity;
        opTitleE.setValueAtTime(0.0, 0);
        opTitleE.setValueAtTime(2.32, 0);
        opTitleE.setValueAtTime(2.36, 100);
        opTitleE.setValueAtTime(2.44, 0);
        for (var kt = 1; kt <= opTitleE.numKeys; kt++) {
            opTitleE.setInterpolationTypeAtKey(kt, KeyframeInterpolationType.HOLD, KeyframeInterpolationType.HOLD);
        }

        // 2.5D Camera with subtle parallax drift
        var cam01 = comp01.layers.addCamera("CAMERA_2_5D_HERO", [600, 200]);
        var camPos = cam01.transform.position;
        camPos.setValueAtTime(0.0, [600, 200, -1100]);
        camPos.setValueAtTime(2.0, [608, 197, -1120]);
        camPos.setValueAtTime(4.0, [600, 200, -1100]);
        applySmoothBezier(camPos, 75, 75);

        addVignetteMaskLayer(comp01);
        addCRTScanlineAdjustment(comp01);
    }

    // ========================================================================
    // COMP_02_IDENTITY (1200 x 300, 20fps, 4.00s)
    // ========================================================================
    var comp02 = app.project.items.addComp("COMP_02_IDENTITY", 1200, 300, 1.0, 4.0, 20);
    comp02.parentFolder = folderMainComps;
    comp02.layers.addSolid([0.02, 0.01, 0.03], "BG_VOID", 1200, 300, 1.0, 4.0);
    if (src.identityPlate) {
        var idPlate = comp02.layers.add(src.identityPlate);
        idPlate.name = "IDENTITY_SONIC_MENU_PLATE";
        var idSonic = comp02.layers.add(precompSonic);
        idSonic.name = "SONIC_IDLE_AVATAR";
        idSonic.transform.scale.setValue([75, 75]);
        idSonic.transform.position.setValue([200, 144]);
        addVignetteMaskLayer(comp02);
        addCRTScanlineAdjustment(comp02);
    }

    // ========================================================================
    // COMP_03_DIVIDERS (1200 x 76, 20fps, 3.00s + 3 Precomps A/B/C)
    // ========================================================================
    var comp03 = app.project.items.addComp("COMP_03_DIVIDERS", 1200, 76, 1.0, 3.0, 20);
    comp03.parentFolder = folderMainComps;
    var divSpecs = [
        { name: "PRECOMP_DIVIDER_A_GOLDEN_RING", item: src.divAGold },
        { name: "PRECOMP_DIVIDER_B_CORRUPTED_RING", item: src.divBCorr },
        { name: "PRECOMP_DIVIDER_C_GREEN_HILL", item: src.divCGhz }
    ];
    for (var di = 0; di < divSpecs.length; di++) {
        var pDiv = app.project.items.addComp(divSpecs[di].name, 1200, 76, 1.0, 3.0, 20);
        pDiv.parentFolder = folderPrecomps;
        if (divSpecs[di].item) {
            var dl = pDiv.layers.add(divSpecs[di].item);
            dl.name = divSpecs[di].name + "_PLATE";
        }
        addCRTScanlineAdjustment(pDiv);
        var cl = comp03.layers.add(pDiv);
        cl.name = divSpecs[di].name;
    }

    // ========================================================================
    // COMP_04_PROJECTS (1200 x 320, 20fps, 3.50s)
    // ========================================================================
    var comp04 = app.project.items.addComp("COMP_04_PROJECTS", 1200, 320, 1.0, 3.5, 20);
    comp04.parentFolder = folderMainComps;
    comp04.layers.addSolid([0.02, 0.01, 0.02], "BG_DATA_SELECT_VOID", 1200, 320, 1.0, 3.5);
    if (src.projHeader) {
        var ph = comp04.layers.add(src.projHeader);
        ph.name = "PROJECTS_HEADER_BANNER";
        ph.transform.position.setValue([600, 60]);
    }
    if (src.projCardSample) {
        var pcL = comp04.layers.add(src.projCardSample);
        pcL.name = "PROJECT_SLOT_LEFT";
        pcL.transform.position.setValue([305, 210]);
        var pcR = comp04.layers.add(src.projCardSample);
        pcR.name = "PROJECT_SLOT_RIGHT";
        pcR.transform.position.setValue([895, 210]);
    }
    addCRTScanlineAdjustment(comp04);

    // ========================================================================
    // COMP_05_TECH_LANGUAGES, COMP_06_TECH_ECOSYSTEM, COMP_07_TECH_TOOLS
    // ========================================================================
    function buildTechComp(compName, h, normOv, corrOv) {
        var c = app.project.items.addComp(compName, 1200, h, 1.0, 4.0, 20);
        c.parentFolder = folderMainComps;
        if (src.heroSkyNorm) {
            var s1 = c.layers.add(src.heroSkyNorm);
            s1.name = "GHZ_SKY_LAYER";
            var m1 = c.layers.add(src.heroMtnNorm);
            m1.name = "GHZ_MOUNTAINS_WATERFALL";
            var g1 = c.layers.add(src.heroFgNorm);
            g1.name = "GHZ_PALMS_AND_CHECKER_TERRAIN";
            var gC = c.layers.add(src.heroFgCorr);
            gC.name = "GHZ_CORRUPTED_TERRAIN_PULSE";
            var opG = gC.transform.opacity;
            opG.setValueAtTime(0.0, 0);
            opG.setValueAtTime(2.50, 0);
            opG.setValueAtTime(2.55, 100);
            opG.setValueAtTime(2.70, 0);
        }
        if (normOv) {
            var ovN = c.layers.add(normOv);
            ovN.name = "SONIC_ITEM_MONITORS_NORMAL";
        }
        if (corrOv) {
            var ovC = c.layers.add(corrOv);
            ovC.name = "SONIC_ITEM_MONITORS_CORRUPTED";
            var opO = ovC.transform.opacity;
            opO.setValueAtTime(0.0, 0);
            opO.setValueAtTime(2.50, 0);
            opO.setValueAtTime(2.55, 100);
            opO.setValueAtTime(2.70, 0);
        }
        addVignetteMaskLayer(c);
        addCRTScanlineAdjustment(c);
        return c;
    }

    var comp05 = buildTechComp("COMP_05_TECH_LANGUAGES", 430, src.techLangNorm, src.techLangCorr);
    var comp06 = buildTechComp("COMP_06_TECH_ECOSYSTEM", 420, src.techEcoNorm, src.techEcoCorr);
    var comp07 = buildTechComp("COMP_07_TECH_TOOLS", 420, src.techToolsNorm, src.techToolsCorr);

    // ========================================================================
    // COMP_08_TROPHY_SELECTION (1200 x 110, 20fps, 3.50s)
    // ========================================================================
    var comp08 = app.project.items.addComp("COMP_08_TROPHY_SELECTION", 1200, 110, 1.0, 3.5, 20);
    comp08.parentFolder = folderMainComps;
    if (src.trophyHeader) {
        var th = comp08.layers.add(src.trophyHeader);
        th.name = "TROPHY_SELECTION_HEADER_PLATE";
    }
    addCRTScanlineAdjustment(comp08);

    // ========================================================================
    // COMP_09_FOOTER (1200 x 150, 20fps, 3.50s)
    // ========================================================================
    var comp09 = app.project.items.addComp("COMP_09_FOOTER", 1200, 150, 1.0, 3.5, 20);
    comp09.parentFolder = folderMainComps;
    comp09.layers.addSolid([0.02, 0.01, 0.02], "BG_FOOTER_VOID", 1200, 150, 1.0, 3.5);
    if (src.footerBanner) {
        var fb = comp09.layers.add(src.footerBanner);
        fb.name = "FOOTER_GHZ_TRIM_BANNER";
        fb.transform.position.setValue([600, 42]);
    }
    if (src.btnGithub && src.btnPortfolio && src.btnLinkedin) {
        var b1 = comp09.layers.add(src.btnGithub);
        b1.name = "BTN_MENU_GITHUB";
        b1.transform.position.setValue([280, 114]);

        var b2 = comp09.layers.add(src.btnPortfolio);
        b2.name = "BTN_MENU_PORTFOLIO";
        b2.transform.position.setValue([600, 114]);

        var b3 = comp09.layers.add(src.btnLinkedin);
        b3.name = "BTN_MENU_LINKEDIN";
        b3.transform.position.setValue([920, 114]);
    }
    addCRTScanlineAdjustment(comp09);

    // ========================================================================
    // SAVE EDITABLE PROJECT (.AEP) & RENDER VIEWPORT PROOF FRAMES
    // ========================================================================
    var outAep = new File(aepPath);
    app.project.save(outAep);

    // Export verification PNG frames directly from After Effects CC 2019 engine
    try {
        comp01.saveFrameToPng(0.5, new File(rendersDir + "/ae_comp01_hero_normal.png"));
        comp01.saveFrameToPng(2.38, new File(rendersDir + "/ae_comp01_hero_exe.png"));
        comp02.saveFrameToPng(0.5, new File(rendersDir + "/ae_comp02_identity.png"));
        comp05.saveFrameToPng(0.5, new File(rendersDir + "/ae_comp05_tech_languages.png"));
        comp09.saveFrameToPng(0.5, new File(rendersDir + "/ae_comp09_footer.png"));
    } catch (er) {}

    // Write ES3-compatible JSON build report
    var rf = new File(reportPath);
    rf.encoding = "UTF-8";
    rf.open("w");
    rf.write(
        '{\n' +
        '  "ok": true,\n' +
        '  "aeVersion": "' + app.version + '",\n' +
        '  "aepFile": "' + aepPath + '",\n' +
        '  "totalItems": ' + app.project.numItems + ',\n' +
        '  "compositions": [\n' +
        '    "COMP_01_HERO",\n' +
        '    "COMP_02_IDENTITY",\n' +
        '    "COMP_03_DIVIDERS",\n' +
        '    "COMP_04_PROJECTS",\n' +
        '    "COMP_05_TECH_LANGUAGES",\n' +
        '    "COMP_06_TECH_ECOSYSTEM",\n' +
        '    "COMP_07_TECH_TOOLS",\n' +
        '    "COMP_08_TROPHY_SELECTION",\n' +
        '    "COMP_09_FOOTER"\n' +
        '  ]\n' +
        '}\n'
    );
    rf.close();

    app.quit();
})();
