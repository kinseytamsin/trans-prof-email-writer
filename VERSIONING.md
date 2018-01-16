Versioning Scheme
=================

trans-prof-email-writer uses the following versioning scheme:

x.y.z[sg]

in which:

- increments in g are unstable
- s is one of 'a' (alpha), 'b' (beta), or 'rc' (release candidate),
  indicating the development stage
- increments in z are stable and mean bug fixes
- increments in y are stable and mean new features
- increments in x are stable, major releases without 100% backward
  compatibility

Only pre-release versions have an `sg` component, and a pre-release
version's main release number signifies the release it's working
towards, so 0.0.5a1 < 0.0.5.
