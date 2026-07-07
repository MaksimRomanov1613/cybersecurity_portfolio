rule file1_rule {
    strings:
        $hex = { D2 47 1F 0A }
        $text = "Malware_A_Signature"
    condition:
        $hex and $text
}
