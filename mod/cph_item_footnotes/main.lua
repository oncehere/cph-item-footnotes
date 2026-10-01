local ccb = rawget(_G, "ccb") or (package and package.loaded and package.loaded["ccb"]) or require("ccb")

if not ccb or not ccb.runtime or not ccb.runtime.hook or not ccb.runtime.handler then
    error("cph_item_footnotes requires CPH with Lua-first Platform runtime support (ccb.runtime missing).")
end

local footnotes = require("data.footnotes_data")
local art_ok, art_data = pcall(require, "data.art_data")
if not art_ok or type(art_data) ~= "table" then
    art_data = { items = {}, variants = {} }
end

local function normalize_lang(lang)
    if not lang or lang == "" then
        return "en"
    end
    local l = string.lower(string.gsub(lang, "-", "_"))
    if string.sub(l, 1, 2) == "zh" then
        return "zh"
    end
    return "en"
end

local function on_description_append(payload)
    if not payload or not payload.item_id then
        return nil
    end

    local effective_lang = normalize_lang(payload.language)
    local text = nil

    if payload.variant_id and payload.variant_id ~= "" and footnotes.variants then
        local vkey = payload.item_id .. ":" .. payload.variant_id
        local variant_entry = footnotes.variants[vkey]
        if variant_entry then
            text = variant_entry[effective_lang] or variant_entry["zh"] or variant_entry["en"]
        end
    end

    if (not text or text == "") and footnotes.items then
        local item_entry = footnotes.items[payload.item_id]
        if item_entry then
            text = item_entry[effective_lang] or item_entry["zh"] or item_entry["en"]
        end
    end

    if text and text ~= "" then
        return { text = text }
    end
    return nil
end

local function on_ascii_art_fallback(payload)
    if not payload or not payload.item_id then
        return nil
    end

    local art_id = nil

    if payload.variant_id and payload.variant_id ~= "" and art_data.variants then
        local vkey = payload.item_id .. ":" .. payload.variant_id
        art_id = art_data.variants[vkey]
    end

    if not art_id and art_data.items then
        art_id = art_data.items[payload.item_id]
    end

    if art_id and art_id ~= "" then
        return { art_id = art_id }
    end
    return nil
end

ccb.runtime.handler("cph_item_footnotes_description_append", on_description_append, 1)
ccb.runtime.handler("cph_item_footnotes_ascii_art_fallback", on_ascii_art_fallback, 1)

local ok, err = pcall(function()
    ccb.runtime.hook("on_item_description_append", "cph_item_footnotes_description_append")
    ccb.runtime.hook("on_item_ascii_art_fallback", "cph_item_footnotes_ascii_art_fallback")
end)
if not ok then
    error("cph_item_footnotes failed to bind native display hooks: " .. tostring(err))
end
