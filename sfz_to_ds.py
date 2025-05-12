import xml.etree.ElementTree as ET
import xml.dom.minidom
from wx_python_out import *
import os
import re

NOTE_NAME_TO_MIDI = {
    'c': 0, 'c#': 1, 'd': 2, 'd#': 3, 'e': 4,
    'f': 5, 'f#': 6, 'g': 7, 'g#': 8, 'a': 9, 'a#': 10, 'b': 11, 'b#': 0
}

EFFECTS = '''  <effects>
    <effect type="lowpass" frequency="22000.0"/>
    <effect type="highpass" frequency="20.0"/>
    <effect type="phaser" mix="0.5" modDepth="0.2" modRate="0.2" centerFrequency="400" feedback="0.7" />
    <effect type="chorus"  mix="0.0" modDepth="0.2" modRate="0.2" />
    <effect type="delay" delayTime="0.7" stereoOffset="0.01" feedback="0.2"/>
    <effect type="reverb" wetLevel="0" roomSize="0.85" damping="0.2"/>
    <effect type="wave_shaper" drive="0.5473124980926514" shape="0.328312486410141" outputLevel="0.1"/>
    <effect type="wave_folder" drive="1" threshold="0.25" />
  </effects>
  <ui width="812" height="375" layoutMode="relative"
      bgMode="top_left">
    <tab name="main">
      <labeled-knob x="25" y="80" width="90" textSize="16" textColor="AA000000"
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999"
                    label="Attack" type="float" minValue="0.0" maxValue="4.0" value="0.01" >
        <binding type="amp" level="instrument" position="0" parameter="ENV_ATTACK" />
      </labeled-knob>
      <labeled-knob x="95" y="80" width="90" textSize="16" textColor="AA000000"
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999"
                    label="Release" type="float" minValue="0.0" maxValue="20.0" value="1" >
        <binding type="amp" level="instrument" position="0" parameter="ENV_RELEASE" />
      </labeled-knob>
      <labeled-knob x="25" y="0" width="90" textSize="16" textColor="FF000000"
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999"
                    label="LowPass" type="float" minValue="0" maxValue="1" value="1">
        <binding type="effect" level="instrument" position="0" parameter="FX_FILTER_FREQUENCY"
                 translation="table"
                 translationTable="0,33;0.3,150;0.4,450;0.5,1100;0.7,4100;0.9,11000;1.0001,22000"/>
      </labeled-knob>
      <labeled-knob x="95" y="0" width="90" textSize="16" textColor="FF000000"
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999"
                    label="HighPass" type="float" minValue="0" maxValue="1" value="0">
        <binding type="effect" level="instrument" position="1" parameter="FX_FILTER_FREQUENCY"
                 translation="table"
                 translationTable="0,33;0.3,150;0.4,450;0.5,1100;0.7,4100;0.9,11000;1.0001,22000"/>
      </labeled-knob>
      <labeled-knob x="165" y="0" width="90" textSize="16" textColor="AA000000"
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999"
                    label="Phaser" type="float" minValue="0.0" maxValue="1" value="0" >
        <binding type="effect" level="instrument" position="2" parameter="FX_MIX" />
      </labeled-knob>
      <labeled-knob x="235" y="0" width="90" textSize="16" textColor="AA000000"
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999"
                    label="ModDepht" type="float" minValue="0.0" maxValue="1" value="0.2" >
        <binding type="effect" level="instrument" position="2" parameter="FX_MOD_DEPTH" />
      </labeled-knob>
      <labeled-knob x="305" y="0" width="90" textSize="16" textColor="AA000000"
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999"
                    label="Chorus" type="float" minValue="0.0" maxValue="1" value="0" >
        <binding type="effect" level="instrument" position="3" parameter="FX_MIX" />
      </labeled-knob>
      <labeled-knob x="375" y="0" width="90" textSize="16" textColor="AA000000"
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999"
                    label="ModDepht" type="float" minValue="0.0" maxValue="1" value="0.2" >
        <binding type="effect" level="instrument" position="3" parameter="FX_MOD_DEPTH" />
      </labeled-knob>
      <labeled-knob x="445" y="0" width="90" textSize="16" textColor="AA000000"
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999"
                    label="Delay" type="float" minValue="0.0" maxValue="1" value="0" >
        <binding type="effect" level="instrument" position="4" parameter="FX_WET_LEVEL" />
      </labeled-knob>
      <labeled-knob x="515" y="0" width="90" textSize="16" textColor="AA000000"
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999"
                    label="DelayTime" type="float" minValue="0.0" maxValue="20" value="0.7" >
        <binding type="effect" level="instrument" position="4" parameter="FX_DELAY_TIME" />
      </labeled-knob>
      <labeled-knob x="585" y="0" width="90" textSize="16" textColor="AA000000"
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999"
                    label="Reverb" type="percent" minValue="0" maxValue="100"
                    textColor="FF000000" value="10">
        <binding type="effect" level="instrument" position="5"
                 parameter="FX_REVERB_WET_LEVEL" translation="linear"
                 translationOutputMin="0" translationOutputMax="1" />
      </labeled-knob>
      <labeled-knob x="655" y="0" width="90" textSize="16" textColor="AA000000"
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999"
                    label="RoomSize" type="percent" minValue="0" maxValue="1"
                    textColor="FF000000" value="0.7">
        <binding type="effect" level="instrument" position="5" parameter="FX_REVERB_ROOM_SIZE"/>
      </labeled-knob>
            <labeled-knob x="725" y="0" width="90" textSize="16" textColor="AA000000"
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999"
                    label="Damping" type="percent" minValue="0" maxValue="1"
                    textColor="FF000000" value="0.2">
        <binding type="effect" level="instrument" position="5" parameter="FX_REVERB_DAMPING"/>
      </labeled-knob>
      <labeled-knob x="305" y="80" width="90" textSize="16" textColor="AA000000"
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999" label="Drive(!)" type="float" minValue="1" maxValue="10" textColor="FF000000" value="1">
        <binding type="effect" level="instrument" position="6" parameter="FX_DRIVE" translation="linear"/>
      </labeled-knob>
      <labeled-knob x="375" y="80" width="90" textSize="16" textColor="AA000000"
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999" label="Drive Boost" type="float" minValue="0" maxValue="1" value="0" textColor="FF000000">
        <binding type="effect" level="instrument" position="6" parameter="FX_DRIVE_BOOST" translation="linear"/>
      </labeled-knob>
      <labeled-knob x="445" y="80" width="90" textSize="16" textColor="AA000000"
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999" label="Output Lvl" type="float" minValue="0" maxValue="1" value="0.5" textColor="FF000000">
        <binding type="effect" level="instrument" position="6" parameter="FX_OUTPUT_LEVEL" translation="linear"/>
      </labeled-knob>
      <labeled-knob x="655" y="80" width="90" textSize="16" textColor="AA000000"
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999" label="Folder Drive" type="float" minValue="1" maxValue="50" textColor="FF000000" value="1">
        <binding type="effect" level="instrument" position="7" parameter="FX_DRIVE" translation="linear" />
      </labeled-knob>
      <labeled-knob x="725" y="80" width="90" textSize="16" textColor="AA000000"
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999" label="Threshold" type="float" minValue="0" maxValue="10" value=".25" textColor="FF000000">
        <binding type="effect" level="instrument" position="7" effectIndex="0" parameter="FX_THRESHOLD" translation="linear" />
      </labeled-knob>

    </tab>
  </ui>
</DecentSampler>
'''


def note_to_midi(note_str):
    """Convert note name like 'a1' to MIDI note number."""
    try:
        match = re.match(r'^([a-gA-G]#?)(-?\d)$', note_str.lower())
    except:
        print(f"Invalid note format: {note_str}")
        return None
    if match:
        note, octave = match.groups()
        midi = NOTE_NAME_TO_MIDI[note] + (int(octave) + 1) * 12
        return str(midi)
    elif note_str.isdigit():
        return note_str
    else:
        print(f"Invalid note format: {note_str}")
        return None


def parse_sfz(sfz_path):
    regions = []
    current_region = {}

    with open(sfz_path, "r", encoding="latin-1") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("//"):
                continue

            # New region
            if "<region>" in line:
                if current_region:
                    regions.append(current_region)
                current_region = {}
                line = line.replace("<region>", "").strip()

            # Match key=value pairs including those with unquoted values containing spaces
            # This regex captures key=value groups correctly
            pattern = r'(\w+)=(".*?"|[^\s]+(?:\s(?!\w+=)[^\s]+)*)'
            matches = re.findall(pattern, line)
            for key, value in matches:
                value = value.strip('"')  # remove quotes if present
                current_region[key.lower()] = value

    if current_region:
        regions.append(current_region)

    return regions


def sfz_to_decentsampler(regions, output_path, effects):
    root = ET.Element("DecentSampler", {"pluginVersion": "1"})
    groups = ET.SubElement(root, "groups")
    group = ET.SubElement(groups, "group", {"name": "default"})
    sample_dir = ''
    for region in regions:
        sample_dir = region.get("default_path", sample_dir)
    if sample_dir:
        print(sample_dir)
        sample_dir = sample_dir.replace('../', '')
        print(sample_dir)
    for region in regions:
        sample_path = region.get("sample", "")
        if not sample_path:
            continue  # Skip regions without valid sample
        root_note = note_to_midi(region.get("pitch_keycenter", region.get("key", "60")))
        lo_note = note_to_midi(region.get("lokey", root_note))
        hi_note = note_to_midi(region.get("hikey", root_note))
        if not root_note or not lo_note or not hi_note:
            print(f"Invalid note values in region: {region}")
            continue
        if sample_dir:
            sample_path = sample_dir + sample_path

        ET.SubElement(group, "sample", {
            "path": sample_path,
            "rootNote": root_note,
            "loNote": lo_note,
            "hiNote": hi_note
        })

    # Convert to string and pretty-print with minidom
    rough_string = ET.tostring(root, encoding='utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    if effects:
        pretty_xml = re.sub('</DecentSampler>', EFFECTS, pretty_xml)
    print(pretty_xml)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)


class SfzToDs(MyFrame):
    def __init__(self, *args, **kwds):
        MyFrame.__init__(self, *args, **kwds)
        self.set_size()

    def set_size(self):
        '''Define o tamanho da janela de acordo com o ambiente de trabalho'''
        de = os.environ.get('DESKTOP_SESSION')
        if de == 'plasma': # kde
            self.SetSize((726, 320))
        else: # tested only with 'gnome':
            self.SetSize((765, 360))


    def select_file(self, event):  # wxGlade: MyFrame.<event_handler>
        with wx.FileDialog(self, "Open SFZ file", wildcard="SFZ files (*.sfz)|*.sfz",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_OK:
                path = file_dialog.GetPath()
                self.text_ctrl_file.SetValue(path)


    def run(self, event):
        sfz_file = self.text_ctrl_file.GetValue()
        dir_sfz_file = os.path.dirname(sfz_file)
        output_xml = dir_sfz_file + '/' + self.text_ctrl_name_output.GetValue() + '.dspreset'
        print(output_xml)
        regions = parse_sfz(sfz_file)
        sfz_to_decentsampler(regions, output_xml)#, relative_sample_path)
        wx.MessageBox(f"Conversion complete: {output_xml}", "Info", wx.OK | wx.ICON_INFORMATION)

    def select_folder(self, event):  # wxGlade: MyFrame.<event_handler>
        with wx.DirDialog(self, "Choose directory to scan", "",
                    wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dir_dialog:
            if dir_dialog.ShowModal() == wx.ID_OK:
                path = dir_dialog.GetPath()
                self.text_ctrl_folder.SetValue(path)
        event.Skip()

    def scan_folders(self, event):  # wxGlade: MyFrame.<event_handler>
        files = 0
        for folderName, subfolders, filenames in os.walk(self.text_ctrl_folder.GetValue()):
            print('Scaning folder ' + folderName)

            for subfolder in subfolders:
                print('Scaning Subfolder of ' + folderName + ': ' + subfolder)

            for filename in filenames:
                if filename.endswith('.sfz'):
                    sfz_file = os.path.join(folderName, filename)
                    print('Found SFZ file: ' + sfz_file)
                    regions = parse_sfz(sfz_file)
                    output_xml = os.path.join(folderName, filename.replace('.sfz', '.dspreset'))
                    sfz_to_decentsampler(regions, output_xml, self.checkbox_effects.GetValue())
                    print('Converted to DecentSampler file: ' + output_xml)
                    files += 1
                    print(f'Files found = {files}')
        wx.MessageBox(f"Conversion complete: {files} files", "Info", wx.OK | wx.ICON_INFORMATION)
        event.Skip()


class MyApp(wx.App):
    def OnInit(self):
        self.frame = SfzToDs(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()



