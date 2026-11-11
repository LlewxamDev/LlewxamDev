// ============================================================================
// LLEW MINIMAL TECH SHOWCASE — ADOBE PHOTOSHOP 2022 MASTER PSD BUILDER (.JSX)
// Builds editable, layered .PSD master files for the Crimson & Obsidian
// Minimal Tech Showcase GitHub Profile README:
//   1. photoshop/LLEW_Minimal_Hero_Banner.psd (1200 x 340, Multi-Layer RGBA)
//   2. photoshop/LLEW_Minimal_Project_Showcase.psd (640 x 360, Multi-Layer RGBA)
// ============================================================================

#target photoshop

(function () {
    app.displayDialogs = DialogModes.NO;
    var origRuler = app.preferences.rulerUnits;
    app.preferences.rulerUnits = Units.PIXELS;

    var baseDir = "c:/Users/Evandro/Downloads/portf\u00f3lio_bots/LlewxamDev";
    var srcDir = baseDir + "/after-effects/assets-source-minimal";
    var psDir = baseDir + "/photoshop";

    function makeRGB(r, g, b) {
        var c = new SolidColor();
        c.rgb.red = r;
        c.rgb.green = g;
        c.rgb.blue = b;
        return c;
    }

    function importPngAsLayer(doc, pngPath, layerName) {
        var f = new File(pngPath);
        if (!f.exists) return null;
        var tempDoc = app.open(f);
        tempDoc.activeLayer.duplicate(doc, ElementPlacement.PLACEATBEGINNING);
        tempDoc.close(SaveOptions.DONOTSAVECHANGES);
        app.activeDocument = doc;
        doc.activeLayer.name = layerName;
        return doc.activeLayer;
    }

    // 1. Build LLEW_Minimal_Hero_Banner.psd (1200 x 340)
    var heroDoc = app.documents.add(1200, 340, 72, "LLEW_Minimal_Hero_Banner", NewDocumentMode.RGB, DocumentFill.TRANSPARENT);
    importPngAsLayer(heroDoc, srcDir + "/hero_bg_obsidian_plate.png", "01_BG_OBSIDIAN_AND_CRIMSON_RIM");
    importPngAsLayer(heroDoc, srcDir + "/hero_circuit_traces_plate.png", "02_ARCHITECTURAL_CIRCUIT_TRACES");
    importPngAsLayer(heroDoc, srcDir + "/hero_typography_plate.png", "03_TYPOGRAPHY_EVANDRO_SILVA_AMORIM");

    // Add editable live text note layer (hidden by default so rasterized pixel-locked plate stays crisp)
    var txtLayer = heroDoc.artLayers.add();
    txtLayer.kind = LayerKind.TEXT;
    txtLayer.name = "04_EDITABLE_HEADLINE_SOURCE";
    txtLayer.textItem.contents = "Evandro Silva Amorim";
    txtLayer.textItem.position = [48, 108];
    txtLayer.textItem.size = 42;
    txtLayer.textItem.color = makeRGB(244, 244, 246);
    txtLayer.visible = false;

    var psdOpts = new PhotoshopSaveOptions();
    psdOpts.layers = true;
    psdOpts.embedColorProfile = true;
    heroDoc.saveAs(new File(psDir + "/LLEW_Minimal_Hero_Banner.psd"), psdOpts, true, Extension.LOWERCASE);
    heroDoc.close(SaveOptions.DONOTSAVECHANGES);

    // 2. Build LLEW_Minimal_Project_Showcase.psd (640 x 360)
    var projDoc = app.documents.add(640, 360, 72, "LLEW_Minimal_Project_Showcase", NewDocumentMode.RGB, DocumentFill.TRANSPARENT);
    importPngAsLayer(projDoc, srcDir + "/demo_aegiscore_plate.png", "01_AEGISCORE_BASE_PLATE");
    importPngAsLayer(projDoc, srcDir + "/demo_aegishub_plate.png", "02_AEGISHUB_BASE_PLATE");
    importPngAsLayer(projDoc, srcDir + "/demo_bots_plate.png", "03_SOULLIST_LWXLAB_BASE_PLATE");
    importPngAsLayer(projDoc, srcDir + "/demo_hyperflow_polybech_plate.png", "04_HYPERFLOW_POLYBECH_BASE_PLATE");
    importPngAsLayer(projDoc, srcDir + "/demo_portfolio_webgl_plate.png", "05_PORTFOLIO_WEBGL_BASE_PLATE");

    projDoc.saveAs(new File(psDir + "/LLEW_Minimal_Project_Showcase.psd"), psdOpts, true, Extension.LOWERCASE);
    projDoc.close(SaveOptions.DONOTSAVECHANGES);

    app.preferences.rulerUnits = origRuler;

    var rf = new File(psDir + "/ps_build_report.json");
    rf.encoding = "UTF-8";
    rf.open("w");
    rf.write('{"ok":true,"psVersion":"' + app.version + '","files":["LLEW_Minimal_Hero_Banner.psd","LLEW_Minimal_Project_Showcase.psd"]}\n');
    rf.close();
})();
