import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Dimensions } from 'react-native';
import React, { useState } from 'react';
import { router } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { Feather } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useStore } from '../store/useStore';

const { width } = Dimensions.get('window');

const MOODS = [
  {
    category: 'High Energy Positive',
    items: [
      { id: 'happy', emoji: '😊', label: 'Happy' },
      { id: 'energetic', emoji: '⚡', label: 'Energetic' },
      { id: 'motivated', emoji: '🔥', label: 'Motivated' },
      { id: 'confident', emoji: '💪', label: 'Confident' },
    ]
  },
  {
    category: 'High Energy Negative',
    items: [
      { id: 'angry', emoji: '😤', label: 'Angry' },
      { id: 'anxious', emoji: '😰', label: 'Anxious' },
    ]
  },
  {
    category: 'Low Energy Positive',
    items: [
      { id: 'calm', emoji: '😌', label: 'Calm' },
    ]
  }
];

export default function HomeScreen() {
  const { mood: storeMood, setMood } = useStore();
  const [selectedMood, setSelectedMood] = useState<string | null>(storeMood || 'happy');

  return (
    <LinearGradient 
      colors={['#eef2ff', '#faf5ff', '#ffffff']} 
      style={styles.container}
      locations={[0, 0.3, 0.6]}
    >
      <SafeAreaView style={styles.safeArea}>
        
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.logoText}>MoodBeats</Text>
          <View style={styles.headerIcons}>
            <TouchableOpacity style={styles.iconButton}>
              <Feather name="clock" size={20} color="#4b5563" />
            </TouchableOpacity>
            <TouchableOpacity 
              style={styles.iconButton}
              onPress={() => router.push('/settings')}
            >
              <Feather name="settings" size={20} color="#4b5563" />
            </TouchableOpacity>
          </View>
        </View>

        {/* Scroll Content */}
        <ScrollView 
          showsVerticalScrollIndicator={false}
          contentContainerStyle={styles.scrollContent}
        >
          <Text style={styles.title}>How are you{'\n'}feeling right now?</Text>
          <Text style={styles.subtitle}>Select your current mood to get started</Text>

          {MOODS.map((section) => (
            <View key={section.category} style={styles.section}>
              <Text style={styles.sectionTitle}>{section.category}</Text>
              <View style={styles.grid}>
                {section.items.map((item) => {
                  const isSelected = selectedMood === item.id;
                  return (
                    <TouchableOpacity 
                      key={item.id} 
                      style={[
                        styles.cardContainer,
                        !isSelected && styles.cardShadow
                      ]}
                      activeOpacity={0.8}
                      onPress={() => setSelectedMood(item.id)}
                    >
                      {isSelected ? (
                        <LinearGradient
                          colors={['#FFB703', '#FB8500']}
                          style={styles.card}
                          start={{ x: 0, y: 0 }}
                          end={{ x: 1, y: 1 }}
                        >
                          <Text style={styles.emoji}>{item.emoji}</Text>
                          <Text style={[styles.cardLabel, styles.cardLabelSelected]}>{item.label}</Text>
                        </LinearGradient>
                      ) : (
                        <View style={[styles.card, styles.cardUnselected]}>
                          <Text style={styles.emoji}>{item.emoji}</Text>
                          <Text style={styles.cardLabel}>{item.label}</Text>
                        </View>
                      )}
                    </TouchableOpacity>
                  );
                })}
              </View>
            </View>
          ))}
          
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
              if (selectedMood) setMood(selectedMood);
              router.push('/activitySelection');
            }}
          >
            <LinearGradient
              colors={['#A800FF', '#FF007F']}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 0 }}
              style={styles.continueButton}
            >
              <Text style={styles.continueButtonText}>Continue</Text>
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
  logoText: {
    fontSize: 26,
    fontWeight: '800',
    color: '#D900FF',
    letterSpacing: -0.5,
  },
  headerIcons: {
    flexDirection: 'row',
    gap: 12,
  },
  iconButton: {
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
    marginBottom: 28,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: '#4b5563',
    marginBottom: 16,
  },
  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    rowGap: 16,
  },
  cardContainer: {
    width: '47.5%',
    borderRadius: 24,
  },
  cardShadow: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.05,
    shadowRadius: 12,
    elevation: 2,
  },
  card: {
    paddingVertical: 24,
    paddingHorizontal: 16,
    borderRadius: 24,
    alignItems: 'center',
    justifyContent: 'center',
    height: 120,
  },
  cardUnselected: {
    backgroundColor: '#ffffff',
    borderWidth: 1,
    borderColor: '#f9fafb',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.03,
    shadowRadius: 8,
    elevation: 1,
  },
  emoji: {
    fontSize: 32,
    marginBottom: 12,
  },
  cardLabel: {
    fontSize: 16,
    fontWeight: '700',
    color: '#374151',
  },
  cardLabelSelected: {
    color: '#ffffff',
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