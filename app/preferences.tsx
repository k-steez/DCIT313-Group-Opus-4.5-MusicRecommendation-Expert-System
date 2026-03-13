import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Dimensions } from 'react-native';
import React, { useState } from 'react';
import { router } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { Feather } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useStore } from '../store/useStore';

const { width } = Dimensions.get('window');

const LYRIC_PREFERENCES = [
  { id: 'with_lyrics', label: 'With Lyrics' },
  { id: 'instrumental', label: 'Instrumental' },
  { id: 'no_preference', label: 'No Preference' },
];

const PLAYLIST_LENGTHS = [
  { id: 5, label: '5' },
  { id: 10, label: '10' },
  { id: 15, label: '15' },
  { id: 20, label: '20' },
];

export default function PreferencesScreen() {
  const { lyricPreference: storeLyric, playlistLength: storeLength, setPreferences } = useStore();
  const [lyricPreference, setLyricPreference] = useState<string>(storeLyric || 'with_lyrics');
  const [playlistLength, setPlaylistLength] = useState<number>(storeLength || 10);

  return (
    <LinearGradient 
      colors={['#faf5ff', '#fdfaff', '#ffffff']} 
      style={styles.container}
      locations={[0, 0.4, 0.8]}
    >
      <SafeAreaView style={styles.safeArea}>
        
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity 
            style={styles.backButton}
            onPress={() => router.back()}
          >
            <Feather name="chevron-left" size={24} color="#374151" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Preferences</Text>
          {/* Invisible view for centering the title */}
          <View style={{ width: 44 }} />
        </View>

        {/* Scroll Content */}
        <ScrollView 
          showsVerticalScrollIndicator={false}
          contentContainerStyle={styles.scrollContent}
        >
          <Text style={styles.title}>Fine-tune{'\n'}your{'\n'}experience</Text>
          <Text style={styles.subtitle}>Customize your playlist preferences</Text>

          {/* Lyric Preference Section */}
          <View style={styles.section}>
            <View style={styles.sectionTitleContainer}>
              <Feather name="music" size={20} color="#A800FF" style={styles.sectionIcon} />
              <Text style={styles.sectionTitle}>Lyric Preference</Text>
            </View>

            <View style={styles.radioGroup}>
              {LYRIC_PREFERENCES.map((option) => {
                const isSelected = lyricPreference === option.id;

                return (
                  <TouchableOpacity
                    key={option.id}
                    activeOpacity={0.8}
                    onPress={() => setLyricPreference(option.id)}
                    style={[
                      styles.radioOptionContainer,
                      !isSelected && styles.radioOptionShadow
                    ]}
                  >
                    {isSelected ? (
                      <LinearGradient
                        colors={['#A800FF', '#E4007C']}
                        start={{ x: 0, y: 0 }}
                        end={{ x: 1, y: 0 }}
                        style={styles.radioOption}
                      >
                        <View style={styles.radioCircleSelected}>
                          <View style={styles.radioInnerCircle} />
                        </View>
                        <Text style={[styles.radioLabel, styles.radioLabelSelected]}>
                          {option.label}
                        </Text>
                      </LinearGradient>
                    ) : (
                      <View style={[styles.radioOption, styles.radioOptionUnselected]}>
                        <View style={styles.radioCircle} />
                        <Text style={styles.radioLabel}>{option.label}</Text>
                      </View>
                    )}
                  </TouchableOpacity>
                );
              })}
            </View>
          </View>

          {/* Info Banner */}
          <View style={styles.infoBanner}>
            <Feather name="alert-circle" size={20} color="#D97706" style={styles.infoIcon} />
            <Text style={styles.infoText}>
              For high cognitive focus, instrumental music will be prioritized.
            </Text>
          </View>

          {/* Playlist Length Section */}
          <View style={styles.section}>
            <View style={styles.sectionTitleContainer}>
              <Feather name="clock" size={20} color="#A800FF" style={styles.sectionIcon} />
              <Text style={styles.sectionTitle}>Playlist Length</Text>
            </View>

            <View style={styles.grid}>
              {PLAYLIST_LENGTHS.map((length) => {
                const isSelected = playlistLength === length.id;

                return (
                  <TouchableOpacity
                    key={length.id}
                    activeOpacity={0.8}
                    onPress={() => setPlaylistLength(length.id)}
                    style={[
                      styles.gridItemContainer,
                      !isSelected && styles.gridItemShadow
                    ]}
                  >
                    {isSelected ? (
                      <LinearGradient
                        colors={['#A800FF', '#E4007C']}
                        start={{ x: 0, y: 0 }}
                        end={{ x: 1, y: 1 }}
                        style={styles.gridItem}
                      >
                        <Text style={[styles.gridItemValue, styles.gridItemValueSelected]}>
                          {length.label}
                        </Text>
                        <Text style={[styles.gridItemSubtitle, styles.gridItemSubtitleSelected]}>songs</Text>
                      </LinearGradient>
                    ) : (
                      <View style={[styles.gridItem, styles.gridItemUnselected]}>
                        <Text style={styles.gridItemValue}>{length.label}</Text>
                        <Text style={styles.gridItemSubtitle}>songs</Text>
                      </View>
                    )}
                  </TouchableOpacity>
                );
              })}
            </View>
          </View>

          {/* Bottom spacing for fixed button */}
          <View style={{ height: 120 }} />
        </ScrollView>

        {/* Bottom Fixed Area */}
        <LinearGradient
          colors={['rgba(255,255,255,0)', 'rgba(255,255,255,0.8)', '#ffffff']}
          style={styles.bottomGradient}
          pointerEvents="box-none"
        >
          <TouchableOpacity 
            style={styles.continueButtonContainer} 
            activeOpacity={0.9}
            onPress={() => {
              setPreferences(lyricPreference, playlistLength);
              router.push('/loading');
            }}
          >
            <LinearGradient
              colors={['#A800FF', '#FF007F']}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 0 }}
              style={styles.continueButton}
            >
              <Text style={styles.continueButtonText}>Generate Playlist</Text>
            </LinearGradient>
          </TouchableOpacity>
        </LinearGradient>

      </SafeAreaView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  safeArea: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 24,
    paddingTop: 10,
    paddingBottom: 20,
  },
  backButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: '#ffffff',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
    borderWidth: 1,
    borderColor: '#f9fafb',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: '#1f2937',
  },
  scrollContent: {
    paddingHorizontal: 24,
    paddingBottom: 40,
  },
  title: {
    fontSize: 34,
    fontWeight: '800',
    color: '#1f2937',
    textAlign: 'center',
    marginTop: 10,
    marginBottom: 12,
    lineHeight: 40,
  },
  subtitle: {
    fontSize: 16,
    color: '#6b7280',
    textAlign: 'center',
    marginBottom: 32,
  },
  section: {
    marginBottom: 24,
  },
  sectionTitleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  sectionIcon: {
    marginRight: 8,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#374151',
  },
  radioGroup: {
    gap: 12,
  },
  radioOptionContainer: {
    borderRadius: 16,
  },
  radioOptionShadow: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.04,
    shadowRadius: 6,
    elevation: 1,
  },
  radioOption: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 18,
    borderRadius: 16,
  },
  radioOptionUnselected: {
    backgroundColor: '#ffffff',
    borderWidth: 1,
    borderColor: '#f3f4f6',
  },
  radioCircle: {
    width: 20,
    height: 20,
    borderRadius: 10,
    borderWidth: 2,
    borderColor: '#9ca3af',
    marginRight: 16,
  },
  radioCircleSelected: {
    width: 20,
    height: 20,
    borderRadius: 10,
    borderWidth: 2,
    borderColor: '#ffffff',
    marginRight: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },
  radioInnerCircle: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: '#ffffff',
  },
  radioLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#374151',
  },
  radioLabelSelected: {
    color: '#ffffff',
  },
  infoBanner: {
    flexDirection: 'row',
    backgroundColor: '#fef3c7',
    borderWidth: 1,
    borderColor: '#FDE68A',
    borderRadius: 12,
    padding: 16,
    marginBottom: 32,
    alignItems: 'flex-start',
  },
  infoIcon: {
    marginRight: 12,
    marginTop: 2,
  },
  infoText: {
    flex: 1,
    fontSize: 14,
    color: '#B45309',
    lineHeight: 20,
    fontWeight: '500',
  },
  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    gap: 12, // For spacing if using React Native >= 0.71, otherwise use rowGap/columnGap or margins
  },
  gridItemContainer: {
    width: '48%',
    borderRadius: 16,
    marginBottom: 12, // fallback for wrap gap
  },
  gridItemShadow: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.04,
    shadowRadius: 6,
    elevation: 1,
  },
  gridItem: {
    paddingVertical: 24,
    paddingHorizontal: 16,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
    height: 100,
  },
  gridItemUnselected: {
    backgroundColor: '#ffffff',
    borderWidth: 1,
    borderColor: '#f3f4f6',
  },
  gridItemValue: {
    fontSize: 28,
    fontWeight: '800',
    color: '#1f2937',
    marginBottom: 4,
  },
  gridItemValueSelected: {
    color: '#ffffff',
  },
  gridItemSubtitle: {
    fontSize: 14,
    color: '#6b7280',
    fontWeight: '500',
  },
  gridItemSubtitleSelected: {
    color: '#ffffff',
    opacity: 0.9,
  },
  bottomGradient: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    height: 140,
    justifyContent: 'flex-end',
    paddingHorizontal: 24,
    paddingBottom: 34,
  },
  continueButtonContainer: {
    shadowColor: '#FF007F',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.3,
    shadowRadius: 16,
    elevation: 8,
  },
  continueButton: {
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
  },
  continueButtonText: {
    color: '#ffffff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});
