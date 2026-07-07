rule file3_rule {
    strings:
        $hex = { C0 C4 4D E1 }
        $text = "Malware_C_Signature"
    condition:
        $hex and $text
}
