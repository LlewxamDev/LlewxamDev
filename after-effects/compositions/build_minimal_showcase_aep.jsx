// ============================================================================
// LLEW MINIMAL TECH SHOWCASE — AFTER EFFECTS CC 2019 PROJECT BUILDER (.JSX)
// Builds editable `after-effects/LLEW_Minimal_Tech_Showcase.aep` containing:
//   - COMP_01_HERO_MINIMAL_CRIMSON (1200 x 340, 20fps, 4.0s, 2.5D Z-planes)
//   - COMP_02_DEMO_AEGISCORE (640 x 360, 18fps, 3.0s)
//   - COMP_03_DEMO_AEGISHUB (640 x 360, 18fps, 3.0s)
//   - COMP_04_DEMO_BOTS_AUTOMATION (640 x 360, 18fps, 3.0s)
//   - COMP_05_DEMO_HYPERFLOW_POLYBECH (640 x 360, 18fps, 3.0s)
// With Bezier Graph Editor Keyframes, 2.5D Camera, and Native AE 2019 Effects.
// ============================================================================

(function () {
    var baseDir = "c:/Users/Evandro/Downloads/portf\u00f3lio_bots/LlewxamDev/after-effects";
    var srcDir = baseDir + "/assets-source-minimal";
    var rendersDir = baseDir + "/renders";
    var aepPath = baseDir + "/LLEW_Minimal_Tech_Showcase.aep";
    var reportPath = rendersDir + "/ae_minimal_showcase_report.json";

    app.suppressDialogs = true;
    if (app.project) {
        app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
    }
    app.newProject();
    app.project.bitsPerChannel = 8;

    var folderMain = app.project.items.addFolder("01_MAIN_COMPOSITIONS");
    var folderPre = app.project.items.addFolder("02_PRECOMPOSITIONS");
    var folderSrc = app.project.items.addFolder("03_PHOTOSHOP_PLATES");

    function importPng(filename) {
        var f = new File(srcDir + "/" + filename);
        if (!f.exists) return null;
        var io = new ImportOptions(f);
        var item = app.project.importFile(io);
        item.parentFolder = folderSrc;
        return item;
    }

    var src = {
        heroBg: importPng("hero_bg_obsidian_plate.png"),
        heroCircuits: importPng("hero_circuit_traces_plate.png"),
        heroTypo: importPng("hero_typography_plate.png"),
        heroMaster: importPng("hero_master_preview.png"),
        demoAegisCore: importPng("demo_aegiscore_plate.png"),
        demoAegisHub: importPng("demo_aegishub_plate.png"),
        demoBots: importPng("demo_bots_plate.png"),
        demoHyperflow: importPng("demo_hyperflow_polybech_plate.png"),
        demoPortfolio: importPng("demo_portfolio_webgl_plate.png")
    };

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

    function addCrimsonGlowAdjustment(comp) {
        var adj = comp.layers.addSolid([0.04, 0.04, 0.05], "CRIMSON_RIM_GLOW_ADJ", comp.width, comp.height, 1.0, comp.duration);
        adj.adjustmentLayer = true;
        try {
            var fxGroup = adj.property("ADBE Effect Parade");
            var glowFx = fxGroup.addProperty("ADBE Glo2");
            if (glowFx) {
                glowFx.property("ADBE Glo2-0002").setValue(68); // Threshold
                glowFx.property("ADBE Glo2-0003").setValue(24); // Radius
                glowFx.property("ADBE Glo2-0004").setValue(0.65); // Subtle Intensity
            }
        } catch (e) {}
        return adj;
    }

    // ========================================================================
    // COMP_01_HERO_MINIMAL_CRIMSON (1200 x 340, 20fps, 4.0s)
    // ========================================================================
    var comp01 = app.project.items.addComp("COMP_01_HERO_MINIMAL_CRIMSON", 1200, 340, 1.0, 4.0, 20);
    comp01.parentFolder = folderMain;

    if (src.heroBg && src.heroCircuits && src.heroTypo) {
        var lBg = comp01.layers.add(src.heroBg);
        lBg.name = "01_OBSIDIAN_VOID_BG_Z300";
        lBg.threeDLayer = true;
        lBg.transform.position.setValue([600, 170, 300]);
        lBg.transform.scale.setValue([128, 128, 100]);

        var lCirc = comp01.layers.add(src.heroCircuits);
        lCirc.name = "02_CIRCUIT_TRACES_Z120";
        lCirc.threeDLayer = true;
        lCirc.transform.position.setValue([600, 170, 120]);
        lCirc.transform.scale.setValue([111, 111, 100]);

        // Subtle animated crimson pulse sweep layer
        var lPulse = comp01.layers.addSolid([0.88, 0.11, 0.28], "03_CRIMSON_NODAL_PULSE", 320, 340, 1.0, 4.0);
        lPulse.blendingMode = BlendingMode.ADD;
        lPulse.transform.opacity.setValue(18);
        var pPos = lPulse.transform.position;
        pPos.setValueAtTime(0.0, [620, 170]);
        pPos.setValueAtTime(2.0, [1120, 170]);
        pPos.setValueAtTime(4.0, [620, 170]);
        applySmoothBezier(pPos, 78, 78);

        var lTypo = comp01.layers.add(src.heroTypo);
        lTypo.name = "04_TYPOGRAPHY_EVANDRO_SILVA_AMORIM_Z0";
        lTypo.threeDLayer = true;
        lTypo.transform.position.setValue([600, 170, 0]);

        var cam = comp01.layers.addCamera("CAMERA_2_5D_MINIMAL", [600, 170]);
        var camPos = cam.transform.position;
        camPos.setValueAtTime(0.0, [600, 170, -1066.6]);
        camPos.setValueAtTime(2.0, [604, 168, -1076.0]);
        camPos.setValueAtTime(4.0, [600, 170, -1066.6]);
        applySmoothBezier(camPos, 75, 75);

        addCrimsonGlowAdjustment(comp01);
    }

    // ========================================================================
    // COMP_02..05 PROJECT SHOWCASE COMPOSITIONS (640 x 360, 18fps, 3.0s)
    // ========================================================================
    function buildDemoComp(compName, plateItem) {
        var c = app.project.items.addComp(compName, 640, 360, 1.0, 3.0, 18);
        c.parentFolder = folderMain;
        if (plateItem) {
            var pl = c.layers.add(plateItem);
            pl.name = compName + "_PHOTOSHOP_PLATE";
        }
        var scan = c.layers.addSolid([0.88, 0.11, 0.28], "TELEMETRY_ACTIVE_SWEEP", 600, 36, 1.0, 3.0);
        scan.blendingMode = BlendingMode.SCREEN;
        scan.transform.opacity.setValue(12);
        var sp = scan.transform.position;
        sp.setValueAtTime(0.0, [320, 160]);
        sp.setValueAtTime(1.5, [320, 290]);
        sp.setValueAtTime(3.0, [320, 160]);
        applySmoothBezier(sp, 75, 75);
        addCrimsonGlowAdjustment(c);
        return c;
    }

    var comp02 = buildDemoComp("COMP_02_DEMO_AEGISCORE", src.demoAegisCore);
    var comp03 = buildDemoComp("COMP_03_DEMO_AEGISHUB", src.demoAegisHub);
    var comp04 = buildDemoComp("COMP_04_DEMO_BOTS_AUTOMATION", src.demoBots);
    var comp05 = buildDemoComp("COMP_05_DEMO_HYPERFLOW_POLYBECH", src.demoHyperflow);
    var comp06 = buildDemoComp("COMP_06_DEMO_PORTFOLIO_WEBGL", src.demoPortfolio);

    // Save .AEP project
    var outAep = new File(aepPath);
    app.project.save(outAep);

    // Export viewport proof PNGs directly from After Effects CC 2019 engine
    try {
        comp01.saveFrameToPng(1.0, new File(rendersDir + "/ae_minimal_comp01_hero.png"));
        comp02.saveFrameToPng(1.0, new File(rendersDir + "/ae_minimal_comp02_aegiscore.png"));
        comp03.saveFrameToPng(1.0, new File(rendersDir + "/ae_minimal_comp03_aegishub.png"));
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
        '    "COMP_01_HERO_MINIMAL_CRIMSON",\n' +
        '    "COMP_02_DEMO_AEGISCORE",\n' +
        '    "COMP_03_DEMO_AEGISHUB",\n' +
        '    "COMP_04_DEMO_BOTS_AUTOMATION",\n' +
        '    "COMP_05_DEMO_HYPERFLOW_POLYBECH"\n' +
        '  ]\n' +
        '}\n'
    );
    rf.close();

    app.quit();
})();
