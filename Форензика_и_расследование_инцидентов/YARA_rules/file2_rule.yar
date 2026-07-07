rule file2_rule {
    strings:
        $hex = { 78 60 A2 96 }
        $text = "Malware_B_Signature"
    condition:
        filesize < 600KB and $hex and $text
}
